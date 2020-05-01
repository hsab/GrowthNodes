
# GrowthNodes

### An Iterative Approach to Simulation of Organic Growth on Surfaces Using Displacement and Procedural Textures

GrowthNodes is a Blender plugin for generative content creation and simulation of organic growth processes on polygonal surfaces. It is based on an iterative approach to simulation of organic growth on surfaces using displacement and procedural textures.

<b>[Download 2.8](https://github.com/hsab/GrowthNodes/archive/master.zip)</b>   
<b>[Download 2.7](https://github.com/hsab/GrowthNodes/archive/2.7.zip)</b>

![Compilation](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/compil.gif)

GrowthNodes is a Blender plugin for generative content creation and simulation of organic growth processes on polygonal surfaces. It can be utilized for both destructive and non-destructive content generation. Simulation is stored as a series of shapekeys which allows fine grain control over the baked data and enables easy transferring of blend files from one user to another.

 - [Video Overview](#video-overview)
 - [Background](#background)
 - [Branches & Features](#branches--features)
 - [Usage](#usage)
 - [Targeted Geometry](#targeted-geometry)
 - [Future Plans](#future-plans)

## Video Overview

<a href="https://youtu.be/FAKYwJyKOMM" rel="nofollow" target="_blank"><img src="https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/playvid.gif" alt="Watch video" style="max-width:100%;"></a>

## Background

I was inspired by [Computational Growth by Deskriptiv and Wanderers by Mediated Matter](http://matter.media.mit.edu/environments/details/wanderers-wearables-for-interplanetary-pilgrims) to create a surface based growth simulation toolkit. The addon can be used for a wide range of content creation, including but not limited to the generation of geological, organic/non-organic, fungal, molecular, microscopic, and macroscopic features.

![Created with master branch](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/spheres.gif)

## Branches & Features

The master branch is maintained against the latest version of blender and contains only the features whose maintenance and future development proves feasible. Much is borrowed from [Animation Nodes](https://github.com/JacquesLucke/animation_nodes) developed by [Jacques Lucke](https://twitter.com/jacqueslucke?lang=en) for nodetree management. His addon was inspirational in how GrowthNodes approaches user interactivity.

The master branch includes the following nodes and features:

 - Mesh objects
 - Procedural Textures (Blender Internal Textures)
 - Image Textures
 - Vertex Groups
 - Shapekeys
 - Animation
 - Geometry Displacement
 - Geometry Dissolve
 - Geometry Subdivide
 - Slope Detection
 - Crease Detection
 - Integer, Float, and Boolean Operations

![Created with master branch](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/plane1.gif)

The experimental branch has many additional features that require compilation, external python modules, are not fully tested, and are often hacky. Moreover since development on this branch has been halted, it only works in **Blender 2.76-2.78**. However this branch deserves much attention as it offers advanced and optimized features beyond what Blender could provide. These are:

 - GPU computed [Gray-Scott Reaction Diffusion](https://mrob.com/pub/comp/xmorphia/)
 - Support for both 2D and 3D (solid) textures. 
 - Cython optimizations
 - An experimental engine implemented in Cython without calling Blender's Mesh API with up to 50x performance boost for select operations.

![Created with experimental RD](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/plane2.gif)


## Usage

GrowthNodes uses Blender's PyNodes API to facilitate user interaction. Functions and data blocks are represented as self-contained nodes. Such an approach allows for scalable and user centric design.

 ![enter image description here](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/nodes.gif)

## Targeted Geometry

GrowthNodes can behave intelligently with regards to existing geometry. User is able to select specific regions based on geometric attributes such face slopes or the angle of crevices. Furthermore one can introduce additional detail by subdividing specific regions on the fly and apply growth only to selected regions. Essentially these are simplified yet powerful utilities to obtain dynamic topology.

![Coral growth simulation on text](https://raw.githubusercontent.com/hsab/GrowthNodes/gifs/gifs/suz.gif)
 
## Future Plans

 - Intersection prevention
 - Correct texture preview
 - Additional parameters fo targeting geometry
 - Persistent vertex groups
 - Mesh sequence export

If you have any suggestions feel free to contact me @hiradsab on twitter.
