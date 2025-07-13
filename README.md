# OpenCellLab (OCL)
Open and modular asynchronous cell automata simulator.
This project started as a part of my master's thesis.
There are no functional modules included in this repository! To check or download example modules, go to: https://github.com/m-machala/OpenCellLab-Modules

## What is OCL?
OCL is a cellular automata simulator written in Python 3, which is able to dynamically load user-created modules. 

Its main focus is to make it easy to create, share and use modules, which can add new renderers, environments and cell types to the simulator.

## What do I need to run OCL?
All you need to run the simulator is for python 3 and for PyQt6 to be installed.
Modules may need other libraries determined by their authors for you to be able to run them.

## What kind of cellular automata does OCL simulate?
OCL has been created with asynchronous cellular automata in mind, meaning that each cell is executed individually, instead of executing all cells at the same time, like in other, more popular, CA.

World topology, environmental behavior and cell behavior is determined by the combination of modules you choose. The simulator currently contains a simple 2D renderer, a simple 2D environment and a few cell types you can play around with, but you are free to try making your own!

## How do modules work?
Modules extend what the simulator can do. 

There are three types of modules you can create:
### Renderer
A renderer draws what is happening in the simulation. The only requirement for a renderer is that it can output an image at the specified resolution.

### Environment
An environment answers the questions of cells about their surroundings. Cells call upon the environment to perform actions, like spawning new cells or dying. Each environment is built for a specific renderer.

### Cell pack
Cell packs are a collection of cells. A cell decides what it wants to do, and performs these actions using the environment. Each cell has its internal "cell brain" in which it can store important information for its own use (like its current state or the direction it is "facing"). No other object can touch anything in the cell brain. Cells also have "cell data", which the environment uses to keep track of its own important information about the cells (like position or health). Cells can't directly interact with other cells, they have to do so indirectly through the environment. This makes it so that cells have to follow the rules of the environment and can't break them. Cells are built for a specific environment.

## How to create my own modules?
Creating your own modules is simple. Go to /src/base_classes where you will find a collection of .py and .json files needed to create all of the module types. Each .py file has comments that will explain all of the functions and their uses. Inherit from these packages to be able to use them.

Each module needs a .json file which provides the simulator with the necessary information to load this module and show its info to the users. Use the files from base_classes as a templte for your own starting point.

Mandatory fields for the metadata files are:
"package type" - all packages - specifies which type of package this file is for (renderer, environment, cell)
"package path" - all packages - specifies where the .py file is located relative to the .json file
"package class" - renderers/environments - name of the class which you want to import into the simulation
"package name" - all packages - name of the package which will be shown in the simulation
"cell types" - cell packs - list of cell types, each with its own set of fields
  "cell class" - cell packs - name of the class of the current cell which you want to import into the simulation
  "cell name" - cell packs - name of the current cell which will be shown in the simulation


