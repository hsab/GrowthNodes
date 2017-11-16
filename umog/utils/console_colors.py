# import platform

# import logging
# logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

# ############################################################################
# # Global variables here.
# ############################################################################
# PREFIX = "  "
# CONSOLE_PREFIX = ""
# CONSOLE_HANDLE = None
# CONSOLE_COLOR_CLEAR = None
# DEBUG = True
# LOGGING = True

# def toConsole(passedItem):
#     global DEBUG, LOGGING, CONSOLE_HANDLE, CONSOLE_PREFIX
        
#     if DEBUG == True:
#         if platform.system() == "Windows":
#             # Turn on colorization.
#             ctypes.windll.kernel32.SetConsoleTextAttribute(CONSOLE_HANDLE, FOREGROUND_GREEN)
                
#         if LOGGING == True:
#             if platform.system() == "Windows":
#                 print("test")
#             else:
#                 #Linux or OSX.
#                 logging.debug(bcolors.WARNING + passedItem)
                
        
#         if platform.system() == "Windows":
#             # Turn off colorization.
#             ctypes.windll.kernel32.SetConsoleTextAttribute(CONSOLE_HANDLE, CONSOLE_COLOR_CLEAR)
    

# if (platform.system() == "Linux") or (platform.system() == "Darwin"):
#     # For Linux or OSX, we only need to use ansii escape codes.
#     class bcolors:
#         HEADER = '\033[95m'
#         OKBLUE = '\033[94m'
#         OKGREEN = '\033[92m'
#         WARNING = '\033[93m'
#         FAIL = '\033[91m'
#         ENDC = '\033[0m'
    
#         def disable(self):
#             self.HEADER = ''
#             self.OKBLUE = ''
#             self.OKGREEN = ''
#             self.WARNING = ''
#             self.FAIL = ''
#             self.ENDC = ''

# if platform.system() == "Windows":
#     # For windows we need to use ctypes win32.dll
#     import ctypes
    
#     # Constants from the Windows API
#     STD_OUTPUT_HANDLE = -11
#     FOREGROUND_BLUE_DRK    = 0x0001 # text color contains dark blue.
#     FOREGROUND_GREEN_DRK    = 0x0002 # text color contains green.
#     FOREGROUND_CYAN_DRK    = 0x0003 # text color contains cyan.
#     FOREGROUND_RED_DRK    = 0x0004 # text color contains red.
#     FOREGROUND_PLUM = 0x0005 # text color contains purple.
#     FOREGROUND_GOLD    = 0x0006 # text color contains gold.
#     FOREGROUND_WHITE    = 0x0007 # text color contains white.
#     FOREGROUND_GREY    = 0x0008 # text color contains grey.
#     FOREGROUND_BLUE    = 0x0009 # text color contains blue.
#     FOREGROUND_IVORY    = 0x000f # text color contains ivory.
#     FOREGROUND_YELLOW    = 0x000e # text color contains yellow.
#     FOREGROUND_PINK    = 0x000d # text color contains pink.
#     FOREGROUND_RED    = 0x000c # text color contains red.
#     FOREGROUND_CYAN    = 0x000b # text color contains cyan.
#     FOREGROUND_GREEN    = 0x000a # text color contains green.
    
    
#     def get_csbi_attributes(handle):
#         # Based on IPython's winconsole.py, written by Alexander Belchenko
#         import struct
#         csbi = ctypes.create_string_buffer(22)
#         res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
#         assert res
    
#         (bufx, bufy, curx, cury, wattr,
#         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
#         return wattr

#     CONSOLE_HANDLE = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
#     try:
#         CONSOLE_COLOR_CLEAR = get_csbi_attributes(CONSOLE_HANDLE)
#     except:
#         pass
    
# toConsole("My string and my #" + str(10) +".")
# print("here")