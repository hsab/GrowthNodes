# Unified Model of Organic Growth
A Blender plugin for generative content creation and simulation of organic growth processes.

Inspired by Computational Growth by Deskriptiv and Wanderers by Mediated Matter. 

All prototype photos courtesy of Mediated Matter Group as desirable outcome of the stable release of plugin.

![](http://i.imgur.com/uPNijRm.jpg)

Introduction:
-------------
This project aims to create a plugin for an existing 3D software suit, namely [Blender.](https://en.wikipedia.org/wiki/Blender_(software)) The plugin would allow users to replicate a wide variety of organic structures occurring in nature using a unified mathematical model. The unified model itself is a collection of different subsystems such as those listed below while allowing the user to add their own system as well:

*   Rules-Based System and Equation-Based System
*   Finite Difference Scheme and Cellular Automata
*   Cellular Automata for Reaction-Diffusion Systems
*   Cellular Automata for the Wave Equation

Our project aims to be versatile and out-reaching allowing the user to create structures that are dynamically generated with resemblance to [real-life phenomenon](https://en.wikipedia.org/wiki/Patterns_in_nature) such as Coral Reefs, Bacteria, Crystals, Trees, Branches, Flowers, etc.

![](http://i.imgur.com/ZbtVIuv.jpg)


Technicalities:
--------------
Implementation and algorithms will be heavily inspired by chapter 18 of [Handbook of Bioinspired Algorithms and Applications](https://www.crcpress.com/Handbook-of-Bioinspired-Algorithms-and-Applications/Olariu-Zomaya/p/book/9781584884750) and will utilize complex preexisting libraries and functionalities available in Blender, such as [Dynamic Topology](https://wiki.blender.org/index.php/Dev:Ref/Release_Notes/2.66/Dynamic_Topology_Sculpting) ([Paper 1](http://www.sciencedirect.com/science/article/pii/S0097849311000720) / [Paper 2](https://farsthary.files.wordpress.com/2011/10/dynamic-subdivision-sculpting-final.pdf)) and native [Sculpting](https://docs.blender.org/manual/en/dev/sculpt_paint/sculpting/index.html)functionalities and APIs.

![](http://edge-loop.com/images/blender/DyntopoSculptImprov_20141017_timelapse.gif)

We are hoping to implement the UI using Blender's existing node system, [PyNodes](https://wiki.blender.org/index.php/Dev:Ref/Release_Notes/2.67/Python_Nodes), to allow for visual programming. However the feasibility and possibility of this needs to be analyzed in relation to UI/UX and ease of use.

![](http://blenderpower.com.br/wp-content/uploads/2014/12/Frames.gif)


Userbase & Outreach
-------------------
We are also excited to be tapping into an existing userbase, considering that in 2016 alone Blender had over [7 million downloads](http://download.blender.org/institute/2016Analytics.pdf); 6 million of which were _unique_. Also there is an existing userbase that has been growing since 2002\. Thus the potential for outreach is immense. 

Inspiration
-----------
This project was inspired by a [video](https://www.youtube.com/watch?v=9HI8FerKr6Q) released by [deskriptiv](http://www.deskriptiv.de/) in collaboration with [Mediated Matter Group](http://matter.media.mit.edu/) at MIT investigating the possibilities of [Wearables for Interplanetary Travels](https://www.behance.net/gallery/21605971/Neri-Oxman-Wanderers). However neither a paper nor source code have been published in regards to this and all that exists publicly is the linked video.

![](http://i.imgur.com/5NNxsrd.png)

Release & Future Plans
----------------------
We believed that this model and its possibilities must be shared in an open and constructive environment as it opens many opportunities for professionals in motion and game industries, researchers in biological and mathematical fields and enthusiasts and those that are genuinely curious.

Thus we decided to develop the system for Blender which has been an open-source project since 2002 and one of the biggest advocates of open-source mentality in the industry, while delivering a truly competitive and lean software in comparison to other proprietary suites such as Maya, 3Ds Max, Modo, C4D, etc.  

After completion, the project will be shared as open-source and will be proposed to Blender Foundation to be included as an official addon in their library, which in turn will attract more developers and enthusiasts to jump on board.

Team Members
----------------------
*   Jacob Luke
*   Micah Johnston
*   Marsh Poulson IV
*   Hirad Sabaghian
