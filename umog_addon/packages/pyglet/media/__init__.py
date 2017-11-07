# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
# $Id$

'''Audio and video playback.

pyglet can play WAV files, and if AVbin is installed, many other audio and
video formats.

Playback is handled by the `Player` class, which reads raw data from `Source`
objects and provides methods for pausing, seeking, adjusting the volume, and
so on.  The `Player` class implements the best available audio device
(currently, only OpenAL is supported)::

    player = Player()

A `Source` is used to decode arbitrary audio and video files.  It is
associated with a single player by "queuing" it::

    source = load('background_music.mp3')
    player.queue(source)

Use the `Player` to control playback.

If the source contains video, the `Source.video_format` attribute will be
non-None, and the `Player.texture` attribute will contain the current video
image synchronised to the audio.

Decoding sounds can be processor-intensive and may introduce latency,
particularly for short sounds that must be played quickly, such as bullets or
explosions.  You can force such sounds to be decoded and retained in memory
rather than streamed from disk by wrapping the source in a `StaticSource`::

    bullet_sound = StaticSource(load('bullet.wav'))

The other advantage of a `StaticSource` is that it can be queued on any number
of players, and so played many times simultaneously.

pyglet relies on Python's garbage collector to release resources when a player
has finished playing a source. In this way some operations that could affect
the application performance can be delayed.

The player provides a `Player.delete()` method that can be used to release
resources immediately. Also an explicit call to `gc.collect()`can be used to
collect unused resources.

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import atexit
import ctypes
import heapq
import sys
import threading
import time
import warnings

import pyglet
from pyglet.compat import bytes_type, BytesIO

_debug = pyglet.options['debug_media']

class MediaException(Exception):
    pass

class MediaFormatException(MediaException):
    pass

class CannotSeekException(MediaException):
    pass

class MediaThread(object):
    '''A thread that cleanly exits on interpreter shutdown, and provides
    a sleep method that can be interrupted and a termination method.

    :Ivariables:
        `condition` : threading.Condition
            Lock condition on all instance variables. 
        `stopped` : bool
            True if `stop` has been called.

    '''
    _threads = set()
    _threads_lock = threading.Lock()

    def __init__(self, target=None):
        self._thread = threading.Thread(target=self._thread_run)
        self._thread.setDaemon(True)

        if target is not None:
            self.run = target

        self.condition = threading.Condition()
        self.stopped = False

    @classmethod
    def _atexit(cls):
        with cls._threads_lock:
            threads = list(cls._threads)
        for thread in threads:
            thread.stop()

    def run(self):
        pass

    def _thread_run(self):
        if pyglet.options['debug_trace']:
            pyglet._install_trace()

        with self._threads_lock:
            self._threads.add(self)
        self.run()
        with self._threads_lock:
            self._threads.remove(self)

    def start(self):
        self._thread.start()

    def stop(self):
        '''Stop the thread and wait for it to terminate.

        The `stop` instance variable is set to ``True`` and the condition is
        notified.  It is the responsibility of the `run` method to check
        the value of `stop` after each sleep or wait and to return if set.
        '''
        if _debug:
            print('MediaThread.stop()')
        with self.condition:
            self.stopped = True
            self.condition.notify()
        self._thread.join()

    def sleep(self, timeout):
        '''Wait for some amount of time, or until notified.

        :Parameters:
            `timeout` : float
                Time to wait, in seconds.

        '''
        if _debug:
            print('MediaThread.sleep(%r)' % timeout)
        with self.condition:
            self.condition.wait(timeout)

    def notify(self):
        '''Interrupt the current sleep operation.

        If the thread is currently sleeping, it will be woken immediately,
        instead of waiting the full duration of the timeout.
        '''
        if _debug:
            print('MediaThread.notify()')
        with self.condition:
            self.condition.notify()

atexit.register(MediaThread._atexit)

class WorkerThread(MediaThread):
    def __init__(self, target=None):
        super(WorkerThread, self).__init__(target)
        self._jobs = []

    def run(self):
        while True:
            job = self.get_job()
            if not job:
                break
            job()

    def get_job(self):
        with self.condition:
            while self._empty() and not self.stopped:
                self.condition.wait()
            if self.stopped:
                result = None
            else:
                result = self._get()
        return result
        
    def put_job(self, job):
        with self.condition:
            self._put(job)
            self.condition.notify()

    def clear_jobs(self):
        with self.condition:
            self._clear()
            self.condition.notify()

    def _empty(self):
        return not self._jobs

    def _get(self):
        return self._jobs.pop(0)

    def _put(self, job):
        self._jobs.append(job)

    def _clear(self):
        del self._jobs[:]

class AudioFormat(object):
    '''Audio details.

    An instance of this class is provided by sources with audio tracks.  You
    should not modify the fields, as they are used internally to describe the
    format of data provided by the source.

    :Ivariables:
        `channels` : int
            The number of channels: 1 for mono or 2 for stereo (pyglet does
            not yet support surround-sound sources).
        `sample_size` : int
            Bits per sample; only 8 or 16 are supported.
        `sample_rate` : int
            Samples per second (in Hertz).

    '''

    def __init__(self, channels, sample_size, sample_rate):
        self.channels = channels
        self.sample_size = sample_size
        self.sample_rate = sample_rate
        
        # Convenience
        self.bytes_per_sample = (sample_size >> 3) * channels
        self.bytes_per_second = self.bytes_per_sample * sample_rate

    def __eq__(self, other):
        return (self.channels == other.channels and 
                self.sample_size == other.sample_size and
                self.sample_rate == other.sample_rate)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s(channels=%d, sample_size=%d, sample_rate=%d)' % (
            self.__class__.__name__, self.channels, self.sample_size,
            self.sample_rate)

class VideoFormat(object):
    '''Video details.

    An instance of this class is provided by sources with a video track.  You
    should not modify the fields.

    Note that the sample aspect has no relation to the aspect ratio of the
    video image.  For example, a video image of 640x480 with sample aspect 2.0
    should be displayed at 1280x480.  It is the responsibility of the
    application to perform this scaling.

    :Ivariables:
        `width` : int
            Width of video image, in pixels.
        `height` : int
            Height of video image, in pixels.
        `sample_aspect` : float
            Aspect ratio (width over height) of a single video pixel.
        `frame_rate` : float
            Frame rate (frames per second) of the video.

            AVbin 8 or later is required, otherwise the frame rate will be
            ``None``.

            **Since:** pyglet 1.2.

    '''
    
    def __init__(self, width, height, sample_aspect=1.0):
        self.width = width
        self.height = height
        self.sample_aspect = sample_aspect
        self.frame_rate = None

class AudioData(object):
    '''A single packet of audio data.

    This class is used internally by pyglet.

    :Ivariables:
        `data` : str or ctypes array or pointer
            Sample data.
        `length` : int
            Size of sample data, in bytes.
        `timestamp` : float
            Time of the first sample, in seconds.
        `duration` : float
            Total data duration, in seconds.
        `events` : list of MediaEvent
            List of events contained within this packet.  Events are
            timestamped relative to this audio packet.

    '''
    def __init__(self, data, length, timestamp, duration, events):
        self.data = data
        self.length = length
        self.timestamp = timestamp
        self.duration = duration
        self.events = events

    def consume(self, bytes, audio_format):
        '''Remove some data from beginning of packet.  All events are
        cleared.'''
        self.events = ()
        if bytes == self.length:
            self.data = None
            self.length = 0
            self.timestamp += self.duration
            self.duration = 0.
            return
        elif bytes == 0:
            return

        if not isinstance(self.data, str):
            # XXX Create a string buffer for the whole packet then
            #     chop it up.  Could do some pointer arith here and
            #     save a bit of data pushing, but my guess is this is
            #     faster than fudging aruond with ctypes (and easier).
            data = ctypes.create_string_buffer(self.length)
            ctypes.memmove(data, self.data, self.length)
            self.data = data
        self.data = self.data[bytes:]
        self.length -= bytes
        self.duration -= bytes / float(audio_format.bytes_per_second)
        self.timestamp += bytes / float(audio_format.bytes_per_second)

    def get_string_data(self):
        '''Return data as a string. (Python 3: return as bytes)'''
        if isinstance(self.data, bytes_type):
            return self.data

        buf = ctypes.create_string_buffer(self.length)
        ctypes.memmove(buf, self.data, self.length)
        return buf.raw

class MediaEvent(object):
    def __init__(self, timestamp, event, *args):
        # Meaning of timestamp is dependent on context; and not seen by
        # application.
        self.timestamp = timestamp
        self.event = event
        self.args = args

    def _sync_dispatch_to_player(self, player):
        pyglet.app.platform_event_loop.post_event(player, self.event, *self.args)
        time.sleep(0)
        # TODO sync with media.dispatch_events

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__,
            self.timestamp, self.event, self.args)
    
    def __lt__(self, other):
        return hash(self) < hash(other)

class SourceInfo(object):
    '''Source metadata information.

    Fields are the empty string or zero if the information is not available.

    :Ivariables:
        `title` : str
            Title
        `author` : str
            Author
        `copyright` : str
            Copyright statement
        `comment` : str
            Comment
        `album` : str
            Album name
        `year` : int
            Year
        `track` : int
            Track number
        `genre` : str
            Genre

    :since: pyglet 1.2
    '''

    title = ''
    author = ''
    copyright = ''
    comment = ''
    album = ''
    year = 0
    track = 0
    genre = ''

class Source(object):
    '''An audio and/or video source.

    :Ivariables:
        `audio_format` : `AudioFormat`
            Format of the audio in this source, or None if the source is
            silent.
        `video_format` : `VideoFormat`
            Format of the video in this source, or None if there is no
            video.
        `info` : `SourceInfo`
            Source metadata such as title, artist, etc; or None if the
            information is not available.

            **Since:** pyglet 1.2
    '''

    _duration = None
    
    audio_format = None
    video_format = None
    info = None

    def _get_duration(self):
        return self._duration

    duration = property(lambda self: self._get_duration(),
                        doc='''The length of the source, in seconds.

        Not all source durations can be determined; in this case the value
        is None.

        Read-only.

        :type: float
        ''')

    def play(self):
        '''Play the source.

        This is a convenience method which creates a Player for
        this source and plays it immediately.

        :rtype: `Player`
        '''
        player = Player()
        player.queue(self)
        player.play()
        return player

    def get_animation(self):
        '''Import all video frames into memory as an `Animation`.

        An empty animation will be returned if the source has no video.
        Otherwise, the animation will contain all unplayed video frames (the
        entire source, if it has not been queued on a player).  After creating
        the animation, the source will be at EOS.

        This method is unsuitable for videos running longer than a
        few seconds.

        :since: pyglet 1.1

        :rtype: `pyglet.image.Animation`
        '''
        from pyglet.image import Animation, AnimationFrame
        if not self.video_format:
            return Animation([])
        else:
            frames = []
            last_ts = 0
            next_ts = self.get_next_video_timestamp()
            while next_ts is not None:
                image = self.get_next_video_frame()
                if image is not None:
                    delay = next_ts - last_ts
                    frames.append(AnimationFrame(image, delay))
                    last_ts = next_ts
                next_ts = self.get_next_video_timestamp()
            return Animation(frames)

    def get_next_video_timestamp(self):
        '''Get the timestamp of the next video frame.

        :since: pyglet 1.1

        :rtype: float
        :return: The next timestamp, or ``None`` if there are no more video
            frames.
        '''
        pass

    def get_next_video_frame(self):
        '''Get the next video frame.

        Video frames may share memory: the previous frame may be invalidated
        or corrupted when this method is called unless the application has
        made a copy of it.

        :since: pyglet 1.1

        :rtype: `pyglet.image.AbstractImage`
        :return: The next video frame image, or ``None`` if the video frame
            could not be decoded or there are no more video frames.
        '''
        pass

    # Internal methods that SourceGroup calls on the source:

    def seek(self, timestamp):
        '''Seek to given timestamp.'''
        raise CannotSeekException()

    def _get_queue_source(self):
        '''Return the `Source` to be used as the queue source for a player.

        Default implementation returns self.'''
        return self

    def get_audio_data(self, bytes):
        '''Get next packet of audio data.

        :Parameters:
            `bytes` : int
                Maximum number of bytes of data to return.

        :rtype: `AudioData`
        :return: Next packet of audio data, or None if there is no (more)
            data.
        '''
        return None

class StreamingSource(Source):
    '''A source that is decoded as it is being played, and can only be
    queued once.
    '''
    
    _is_queued = False

    is_queued = property(lambda self: self._is_queued,
                         doc='''Determine if this source has been queued
        on a `Player` yet.

        Read-only.

        :type: bool
        ''')

    def _get_queue_source(self):
        '''Return the `Source` to be used as the queue source for a player.

        Default implementation returns self.'''
        if self._is_queued:
            raise MediaException('This source is already queued on a player.')
        self._is_queued = True
        return self

class StaticSource(Source):
    '''A source that has been completely decoded in memory.  This source can
    be queued onto multiple players any number of times.
    '''
    
    def __init__(self, source):
        '''Construct a `StaticSource` for the data in `source`.

        :Parameters:
            `source` : `Source`
                The source to read and decode audio and video data from.

        '''
        source = source._get_queue_source()
        if source.video_format:
            raise NotImplementedError(
                'Static sources not supported for video yet.')

        self.audio_format = source.audio_format
        if not self.audio_format:
            return

        # Arbitrary: number of bytes to request at a time.
        buffer_size = 1 << 20 # 1 MB

        # Naive implementation.  Driver-specific implementations may override
        # to load static audio data into device (or at least driver) memory. 
        data = BytesIO()
        while True:
            audio_data = source.get_audio_data(buffer_size)
            if not audio_data:
                break
            data.write(audio_data.get_string_data())
        self._data = data.getvalue()

        self._duration = len(self._data) / \
                float(self.audio_format.bytes_per_second)

    def _get_queue_source(self):
        return StaticMemorySource(self._data, self.audio_format)

    def get_audio_data(self, bytes):
        raise RuntimeError('StaticSource cannot be queued.')

class StaticMemorySource(StaticSource):
    '''Helper class for default implementation of `StaticSource`.  Do not use
    directly.'''

    def __init__(self, data, audio_format):
        '''Construct a memory source over the given data buffer.
        '''
        self._file = BytesIO(data)
        self._max_offset = len(data)
        self.audio_format = audio_format
        self._duration = len(data) / float(audio_format.bytes_per_second)

    def seek(self, timestamp):
        offset = int(timestamp * self.audio_format.bytes_per_second)

        # Align to sample
        if self.audio_format.bytes_per_sample == 2:
            offset &= 0xfffffffe
        elif self.audio_format.bytes_per_sample == 4:
            offset &= 0xfffffffc

        self._file.seek(offset)

    def get_audio_data(self, bytes):
        offset = self._file.tell()
        timestamp = float(offset) / self.audio_format.bytes_per_second

        # Align to sample size
        if self.audio_format.bytes_per_sample == 2:
            bytes &= 0xfffffffe
        elif self.audio_format.bytes_per_sample == 4:
            bytes &= 0xfffffffc

        data = self._file.read(bytes)
        if not len(data):
            return None

        duration = float(len(data)) / self.audio_format.bytes_per_second
        return AudioData(data, len(data), timestamp, duration, [])

class SourceGroup(object):
    '''Read data from a queue of sources, with support for looping.  All
    sources must share the same audio format.
    
    :Ivariables:
        `audio_format` : `AudioFormat`
            Required audio format for queued sources.

    '''

    # TODO can sources list go empty?  what behaviour (ignore or error)?

    _advance_after_eos = False
    _loop = False

    def __init__(self, audio_format, video_format):
        self.audio_format = audio_format
        self.video_format = video_format
        self.duration = 0.
        self._timestamp_offset = 0.
        self._dequeued_durations = []
        self._sources = []

    def seek(self, time):
        if self._sources:
            self._sources[0].seek(time)

    def queue(self, source):
        source = source._get_queue_source()
        assert(source.audio_format == self.audio_format)
        self._sources.append(source)
        self.duration += source.duration

    def has_next(self):
        return len(self._sources) > 1

    def next_source(self, immediate=True):
        if immediate:
            self._advance()
        else:
            self._advance_after_eos = True

    #: :deprecated: Use `next_source` instead.
    next = next_source  # old API, worked badly with 2to3

    def get_current_source(self):
        if self._sources:
            return self._sources[0]

    def _advance(self):
        if self._sources:
            self._timestamp_offset += self._sources[0].duration
            self._dequeued_durations.insert(0, self._sources[0].duration)
            old_source = self._sources.pop(0)
            self.duration -= old_source.duration

    def _get_loop(self):
        return self._loop

    def _set_loop(self, loop):
        self._loop = loop        

    loop = property(_get_loop, _set_loop, 
                    doc='''Loop the current source indefinitely or until 
    `next` is called.  Initially False.

    :type: bool
    ''')

    def get_audio_data(self, bytes):
        '''Get next audio packet.

        :Parameters:
            `bytes` : int
                Hint for preferred size of audio packet; may be ignored.

        :rtype: `AudioData`
        :return: Audio data, or None if there is no more data.
        '''

        data = self._sources[0].get_audio_data(bytes)
        eos = False
        while not data:
            eos = True
            if self._loop and not self._advance_after_eos:
                self._timestamp_offset += self._sources[0].duration
                self._dequeued_durations.insert(0, self._sources[0].duration)
                self._sources[0].seek(0)
            else:
                self._advance_after_eos = False

                # Advance source if there's something to advance to.
                # Otherwise leave last source paused at EOS.
                if len(self._sources) > 1:
                    self._advance()
                else:
                    return None
                
            data = self._sources[0].get_audio_data(bytes) # TODO method rename

        data.timestamp += self._timestamp_offset
        if eos:
            if _debug:
                print('adding on_eos event to audio data')
            data.events.append(MediaEvent(0, 'on_eos'))
        return data

    def translate_timestamp(self, timestamp):
        '''Get source-relative timestamp for the audio player's timestamp.'''
        # XXX 
        if timestamp is None:
            return None

        timestamp = timestamp - self._timestamp_offset
        if timestamp < 0:
            for duration in self._dequeued_durations[::-1]:
                timestamp += duration
                if timestamp > 0:
                    break
            assert timestamp >= 0, 'Timestamp beyond dequeued source memory'
        return timestamp

    def get_next_video_timestamp(self):
        '''Get the timestamp of the next video frame.

        :rtype: float
        :return: The next timestamp, or ``None`` if there are no more video
            frames.
        '''
        # TODO track current video source independently from audio source for
        # better prebuffering.
        timestamp = self._sources[0].get_next_video_timestamp()
        if timestamp is not None: 
            timestamp += self._timestamp_offset
        return timestamp

    def get_next_video_frame(self):
        '''Get the next video frame.

        Video frames may share memory: the previous frame may be invalidated
        or corrupted when this method is called unless the application has
        made a copy of it.

        :rtype: `pyglet.image.AbstractImage`
        :return: The next video frame image, or ``None`` if the video frame
            could not be decoded or there are no more video frames.
        '''
        return self._sources[0].get_next_video_frame()

class AbstractAudioPlayer(object):
    '''Base class for driver audio players.
    '''

    def __init__(self, source_group, player):
        '''Create a new audio player.

        :Parameters:
            `source_group` : `SourceGroup`
                Source group to play from.
            `player` : `Player`
                Player to receive EOS and video frame sync events.

        '''
        self.source_group = source_group
        self.player = player

    def play(self):
        '''Begin playback.'''
        raise NotImplementedError('abstract')

    def stop(self):
        '''Stop (pause) playback.'''
        raise NotImplementedError('abstract')

    def delete(self):
        '''Stop playing and clean up all resources used by player.'''
        raise NotImplementedError('abstract')
   
    def _play_group(self, audio_players):
        '''Begin simultaneous playback on a list of audio players.'''
        # This should be overridden by subclasses for better synchrony.
        for player in audio_players:
            player.play()

    def _stop_group(self, audio_players):
        '''Stop simultaneous playback on a list of audio players.'''
        # This should be overridden by subclasses for better synchrony.
        for player in audio_players:
            player.play()

    def clear(self):
        '''Clear all buffered data and prepare for replacement data.

        The player should be stopped before calling this method.
        '''
        raise NotImplementedError('abstract')

    def get_time(self):
        '''Return approximation of current playback time within current source.

        Returns ``None`` if the audio player does not know what the playback
        time is (for example, before any valid audio data has been read).

        :rtype: float
        :return: current play cursor time, in seconds.
        '''
        # TODO determine which source within group
        raise NotImplementedError('abstract')

    def set_volume(self, volume):
        '''See `Player.volume`.'''
        pass

    def set_position(self, position):
        '''See `Player.position`.'''
        pass

    def set_min_distance(self, min_distance):
        '''See `Player.min_distance`.'''
        pass

    def set_max_distance(self, max_distance):
        '''See `Player.max_distance`.'''
        pass

    def set_pitch(self, pitch):
        '''See `Player.pitch`.'''
        pass

    def set_cone_orientation(self, cone_orientation):
        '''See `Player.cone_orientation`.'''
        pass

    def set_cone_inner_angle(self, cone_inner_angle):
        '''See `Player.cone_inner_angle`.'''
        pass

    def set_cone_outer_angle(self, cone_outer_angle):
        '''See `Player.cone_outer_angle`.'''
        pass

    def set_cone_outer_gain(self, cone_outer_gain):
        '''See `Player.cone_outer_gain`.'''
        pass

class Player(pyglet.event.EventDispatcher):
    '''High-level sound and video player.
    '''

    _last_video_timestamp = None
    _texture = None

    # Spacialisation attributes, preserved between audio players
    _volume = 1.0
    _min_distance = 1.0
    _max_distance = 100000000.

    _position = (0, 0, 0)
    _pitch = 1.0

    _cone_orientation = (0, 0, 1)
    _cone_inner_angle = 360.
    _cone_outer_angle = 360.
    _cone_outer_gain = 1.

    #: The player will pause when it reaches the end of the stream.
    #:
    #: :deprecated: Use `SourceGroup.advance_after_eos`
    EOS_PAUSE = 'pause'

    #: The player will loop the current stream continuosly.
    #:
    #: :deprecated: Use `SourceGroup.loop`
    EOS_LOOP = 'loop'

    #: The player will move on to the next queued stream when it reaches the
    #: end of the current source.  If there is no source queued, the player
    #: will pause.
    #:
    #: :deprecated: Use `SourceGroup.advance_after_eos`
    EOS_NEXT = 'next'

    #: The player will stop entirely; valid only for ManagedSoundPlayer.
    #: 
    #: :deprecated: Use `SourceGroup.advance_after_eos`
    EOS_STOP = 'stop'

    #: :deprecated:
    _eos_action = EOS_NEXT

    def __init__(self):
        # List of queued source groups
        self._groups = []

        self._audio_player = None

        # Desired play state (not an indication of actual state).
        self._playing = False

        self._paused_time = 0.0

    def queue(self, source):
        if isinstance(source, SourceGroup):
            self._groups.append(source)
        else:
            if (self._groups and
                source.audio_format == self._groups[-1].audio_format and
                source.video_format == self._groups[-1].video_format):
                self._groups[-1].queue(source)
            else:
                group = SourceGroup(source.audio_format, source.video_format)
                group.queue(source)
                self._groups.append(group)
                self._set_eos_action(self._eos_action)

        self._set_playing(self._playing)

    def _set_playing(self, playing):
        #stopping = self._playing and not playing
        #starting = not self._playing and playing

        self._playing = playing
        source = self.source

        if playing and source:
            if not self._audio_player:
                self._create_audio_player()
            self._audio_player.play()

            if source.video_format:
                if not self._texture:
                    self._create_texture()

                if self.source.video_format.frame_rate:
                    period = 1. / self.source.video_format.frame_rate
                else:
                    period = 1. / 30.
                pyglet.clock.schedule_interval(self.update_texture, period)
        else:
            if self._audio_player:
                self._audio_player.stop()

            pyglet.clock.unschedule(self.update_texture)

    def play(self): 
        self._set_playing(True)

    def pause(self):
        self._set_playing(False)

        if self._audio_player:
            time = self._audio_player.get_time()
            time = self._groups[0].translate_timestamp(time)
            if time is not None:
                self._paused_time = time
            self._audio_player.stop()

    def delete(self):
        self.pause()

        if self._audio_player:
            self._audio_player.delete()
            self._audio_player = None

        while self._groups:
            del self._groups[0]

    def next_source(self):
        if not self._groups:
            return

        group = self._groups[0]
        if group.has_next():
            group.next_source()
            return

        if self.source.video_format:
            self._texture = None
            pyglet.clock.unschedule(self.update_texture)

        if self._audio_player:
            self._audio_player.delete()
            self._audio_player = None

        del self._groups[0]
        if self._groups:
            self._set_playing(self._playing)
            return

        self._set_playing(False)
        self.dispatch_event('on_player_eos')

    #: :deprecated: Use `next_source` instead.
    next = next_source  # old API, worked badly with 2to3

    def seek(self, time):
        if _debug:
            print('Player.seek(%r)' % time)

        self._paused_time = time
        self.source.seek(time)
        if self._audio_player: self._audio_player.clear()
        if self.source.video_format:
            self._last_video_timestamp = None
            self.update_texture(time=time)

    def _create_audio_player(self):
        assert not self._audio_player
        assert self._groups

        group = self._groups[0]
        audio_format = group.audio_format
        if audio_format:
            audio_driver = get_audio_driver()
        else:
            audio_driver = get_silent_audio_driver()
        self._audio_player = audio_driver.create_audio_player(group, self)

        _class = self.__class__
        def _set(name):
            private_name = '_' + name
            value = getattr(self, private_name) 
            if value != getattr(_class, private_name):
                getattr(self._audio_player, 'set_' + name)(value)
        _set('volume')
        _set('min_distance')
        _set('max_distance')
        _set('position')
        _set('pitch')
        _set('cone_orientation')
        _set('cone_inner_angle')
        _set('cone_outer_angle')
        _set('cone_outer_gain')

    def _get_source(self):
        if not self._groups:
            return None
        return self._groups[0].get_current_source()

    source = property(_get_source)

    playing = property(lambda self: self._playing)

    def _get_time(self):
        time = None
        if self._playing and self._audio_player:
            time = self._audio_player.get_time()
            time = self._groups[0].translate_timestamp(time)

        if time is None:
            return self._paused_time
        else:
            return time

    time = property(_get_time)

    def _create_texture(self):
        video_format = self.source.video_format
        self._texture = pyglet.image.Texture.create(
            video_format.width, video_format.height, rectangle=True)
        self._texture = self._texture.get_transform(flip_y=True)
        self._texture.anchor_y = 0

    def get_texture(self):
        return self._texture

    def seek_next_frame(self):
        '''Step forwards one video frame in the current Source.
        '''
        time = self._groups[0].get_next_video_timestamp()
        if time is None:
            return
        self.seek(time)

    def update_texture(self, dt=None, time=None):
        if time is None:
            time = self._audio_player.get_time()
        if time is None:
            return

        if (self._last_video_timestamp is not None and 
            time <= self._last_video_timestamp):
            return

        ts = self._groups[0].get_next_video_timestamp()
        while ts is not None and ts < time:
            self._groups[0].get_next_video_frame() # Discard frame
            ts = self._groups[0].get_next_video_timestamp()

        if ts is None:
            self._last_video_timestamp = None
            return

        image = self._groups[0].get_next_video_frame()
        if image is not None:
            if self._texture is None:
                self._create_texture()
            self._texture.blit_into(image, 0, 0, 0)
            self._last_video_timestamp = ts

    def _set_eos_action(self, eos_action):
        ''':deprecated:'''
        warnings.warn('Player.eos_action is deprecated in favor of SourceGroup.loop and SourceGroup.advance_after_eos',
                      category=DeprecationWarning)
        assert eos_action in (self.EOS_NEXT, self.EOS_STOP, 
                              self.EOS_PAUSE, self.EOS_LOOP)
        self._eos_action = eos_action
        for group in self._groups:
            group.loop = eos_action == self.EOS_LOOP
            group.advance_after_eos = eos_action == self.EOS_NEXT

    eos_action = property(lambda self: self._eos_action,
                          _set_eos_action,
                          doc='''Set the behaviour of the player when it
        reaches the end of the current source.

        This must be one of the constants `EOS_NEXT`, `EOS_PAUSE`, `EOS_STOP` or
        `EOS_LOOP`.

        :deprecated: Use `SourceGroup.loop` and `SourceGroup.advance_after_eos`

        :type: str
        ''')

    def _player_property(name, doc=None):
        private_name = '_' + name
        set_name = 'set_' + name
        def _player_property_set(self, value):
            setattr(self, private_name, value)
            if self._audio_player:
                getattr(self._audio_player, set_name)(value)

        def _player_property_get(self):
            return getattr(self, private_name)

        return property(_player_property_get, _player_property_set, doc=doc)

    # TODO docstrings for these...
    volume = _player_property('volume')
    min_distance = _player_property('min_distance')
    max_distance = _player_property('max_distance')
    position = _player_property('position')
    pitch = _player_property('pitch')
    cone_orientation = _player_property('cone_orientation')
    cone_inner_angle = _player_property('cone_inner_angle')
    cone_outer_angle = _player_property('cone_outer_angle')
    cone_outer_gain = _player_property('cone_outer_gain')

    # Events

    def on_player_eos(self):
        '''The player ran out of sources.

        :event:
        '''
        if _debug:
            print('Player.on_player_eos')

    def on_source_group_eos(self):
        '''The current source group ran out of data.

        The default behaviour is to advance to the next source group if
        possible.

        :event:
        '''
        self.next_source()
        if _debug:
            print('Player.on_source_group_eos')

    def on_eos(self):
        '''

        :event:
        '''
        if _debug:
            print('Player.on_eos')

Player.register_event_type('on_eos')
Player.register_event_type('on_player_eos')
Player.register_event_type('on_source_group_eos')

class ManagedSoundPlayer(Player):
    ''':deprecated: Use `Player`'''
    def __init__(self, *args, **kwargs):
        warnings.warn('Use `Player` instead.', category=DeprecationWarning)
        super(ManagedSoundPlayer, self).__init__(*args, **kwargs)

class PlayerGroup(object):
    '''Group of players that can be played and paused simultaneously.

    :Ivariables:
        `players` : list of `Player`
            Players in this group.

    '''

    def __init__(self, players):
        '''Create a player group for the given set of players.

        All players in the group must currently not belong to any other
        group.

        :Parameters:
            `players` : Sequence of `Player`
                Players to add to this group.

        '''
        self.players = list(players)

    def play(self):
        '''Begin playing all players in the group simultaneously.
        '''
        audio_players = [p._audio_player \
                         for p in self.players if p._audio_player]
        if audio_players:
            audio_players[0]._play_group(audio_players)
        for player in self.players:
            player.play()

    def pause(self):
        '''Pause all players in the group simultaneously.
        '''
        audio_players = [p._audio_player \
                         for p in self.players if p._audio_player]
        if audio_players:
            audio_players[0]._stop_group(audio_players)
        for player in self.players:
            player.pause()

class AbstractAudioDriver(object):
    def create_audio_player(self, source_group, player):
        raise NotImplementedError('abstract')

    def get_listener(self):
        raise NotImplementedError('abstract')

class AbstractListener(object):
    '''The listener properties for positional audio.

    You can obtain the singleton instance of this class by calling
    `AbstractAudioDriver.get_listener`.
    '''
    _volume = 1.0
    _position = (0, 0, 0)
    _forward_orientation = (0, 0, -1)
    _up_orientation = (0, 1, 0)

    def _set_volume(self, volume):
        raise NotImplementedError('abstract')

    volume = property(lambda self: self._volume,
                      lambda self, volume: self._set_volume(volume),
                      doc='''The master volume for sound playback.

        All sound volumes are multiplied by this master volume before being
        played.  A value of 0 will silence playback (but still consume
        resources).  The nominal volume is 1.0.
        
        :type: float
        ''')

    def _set_position(self, position):
        raise NotImplementedError('abstract')

    position = property(lambda self: self._position,
                        lambda self, position: self._set_position(position),
                        doc='''The position of the listener in 3D space.

        The position is given as a tuple of floats (x, y, z).  The unit
        defaults to meters, but can be modified with the listener
        properties.
        
        :type: 3-tuple of float
        ''')

    def _set_forward_orientation(self, orientation):
        raise NotImplementedError('abstract')

    forward_orientation = property(lambda self: self._forward_orientation,
                               lambda self, o: self._set_forward_orientation(o),
                               doc='''A vector giving the direction the
        listener is facing.

        The orientation is given as a tuple of floats (x, y, z), and has
        no unit.  The forward orientation should be orthagonal to the
        up orientation.
        
        :type: 3-tuple of float
        ''')

    def _set_up_orientation(self, orientation):
        raise NotImplementedError('abstract')

    up_orientation = property(lambda self: self._up_orientation,
                              lambda self, o: self._set_up_orientation(o),
                              doc='''A vector giving the "up" orientation
        of the listener.

        The orientation is given as a tuple of floats (x, y, z), and has
        no unit.  The up orientation should be orthagonal to the
        forward orientation.
        
        :type: 3-tuple of float
        ''')

class _LegacyListener(AbstractListener):
    def _set_volume(self, volume):
        get_audio_driver().get_listener().volume = volume
        self._volume = volume

    def _set_position(self, position):
        get_audio_driver().get_listener().position = position
        self._position = position

    def _set_forward_orientation(self, forward_orientation):
        get_audio_driver().get_listener().forward_orientation = \
            forward_orientation
        self._forward_orientation = forward_orientation

    def _set_up_orientation(self, up_orientation):
        get_audio_driver().get_listener().up_orientation = up_orientation
        self._up_orientation = up_orientation

#: The singleton `AbstractListener` object.
#:
#: :deprecated: Use `AbstractAudioDriver.get_listener`
#:
#: :type: `AbstractListener`
listener = _LegacyListener()

class AbstractSourceLoader(object):
    def load(self, filename, file):
        raise NotImplementedError('abstract')

class AVbinSourceLoader(AbstractSourceLoader):
    def load(self, filename, file):
        from . import avbin
        return avbin.AVbinSource(filename, file)

class RIFFSourceLoader(AbstractSourceLoader):
    def load(self, filename, file):
        from . import riff
        return riff.WaveSource(filename, file)
    
def load(filename, file=None, streaming=True):
    '''Load a source from a file.

    Currently the `file` argument is not supported; media files must exist
    as real paths.

    :Parameters:
        `filename` : str
            Filename of the media file to load.
        `file` : file-like object
            Not yet supported.
        `streaming` : bool
            If False, a `StaticSource` will be returned; otherwise (default) a
            `StreamingSource` is created.

    :rtype: `Source`
    '''
    source = get_source_loader().load(filename, file)
    if not streaming:
        source = StaticSource(source)
    return source

def get_audio_driver():
    global _audio_driver

    if _audio_driver:
        return _audio_driver

    _audio_driver = None

    for driver_name in pyglet.options['audio']:
        try:
            if driver_name == 'pulse':
                from .drivers import pulse
                _audio_driver = pulse.create_audio_driver()
                break
            elif driver_name == 'openal':
                from .drivers import openal
                _audio_driver = openal.create_audio_driver()
                break
            elif driver_name == 'directsound':
                from .drivers import directsound
                _audio_driver = directsound.create_audio_driver()
                break
            elif driver_name == 'silent':
                _audio_driver = get_silent_audio_driver()
                break
        except Exception as exp:
            if _debug:
                print('Error importing driver %s:\n%s' % (driver_name, str(exp)))
    return _audio_driver

def get_silent_audio_driver():
    global _silent_audio_driver
    
    if not _silent_audio_driver:
        from .drivers import silent
        _silent_audio_driver = silent.create_audio_driver()

    return _silent_audio_driver

_audio_driver = None
_silent_audio_driver = None

def get_source_loader():
    global _source_loader

    if _source_loader:
        return _source_loader

    try:
        from . import avbin
        _source_loader = AVbinSourceLoader()
    except ImportError:
        _source_loader = RIFFSourceLoader()
    return _source_loader

_source_loader = None

try:
    from . import avbin
    have_avbin = True
except ImportError:
    have_avbin = False
