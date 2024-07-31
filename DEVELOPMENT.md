# The core concept of the program

Since the README.md should contain all needed information on how to **use** this program (or at least the -h/--help argument should be useful), I wanted to use this document here as an explanation on how I meant the code structure to be. There are also doc strings in the class files accordingly. It is also some kind of memory aid for myself, since there is indeed some kind if paradox: I tried very very **VERY** hard to make this code follow all code conventions I know and follow a clear concept of code structure. I somehow fear I made things worse. Yet I am just a non-professional developer to date and do not have much experience. Thus I probably did many things different than a good professional developer would have done. So bla bla, just let me start:

The main idea of the program, thus the code structure as well, is to have documents to be worked with. These documents should have their own folder (relative folders should be possible as well - not tested yet, though). With this and their name, the idea is to have some automatic loading and saving - without the need to specify an absolute filepath. With this base principle I also try to have some kind of automatic list getter, which should be able to e.g. load all documents of a certein document type and list them. This can become handy, when e.g. calculating certain things from invoices.

_So in a nutshell:_

- This program is for creating (and rendering) documents: from YAML to PDF.
- Documents can be of any type, which the user can create.
- The base storing file format is YAML for almost every kind of data.

# The code structure

As already written above: I tried REALYL hard to make this code be easy to understand, very well structured, modular and extendible - even in the future, hopefully. Yet as more I tried to refactor (even when the program was not even finished ... pre-mature, I know) ths program to become even more dynamic, flexible, better structured and easier to understand, I fear that I might have messed up a bit. I fear that the code is unnecessary complicated and bloated, despite the fact that on the ground it's basically just about rendering a YAML to PDF.

Yes, on the core it's basically just that:

> RENDER A YAML TO PDF

**ANY**way: The core concept tries to follow the MVC principle:

> Model + View + Controller

Thus I came up with the following strucutre. And I might have forgot something or maybe not mention it, because it was not final. Also I might forget something in the future, in case I extend the program yet forget about adding new objects or so here. The order of the classes is _Model > View > Controller_ and inside the section it is alphabetically.

## Model

These models try to implement the core logic of the program. Let me try to give a tree view of the structure. The root is the class I want to describe and it has the parents in the square brackets. Its childs are the components, which hold other classes. I will not list the attributes, which are variables only, because I would forget to update them for sure here. The goal is to visualize the structure only. After that tree I will explain the classes itself. All sorted by dependency:

- DataModel

### DataModel

This object is the parent of the Document and the DocumentType class. It combines the logic of parsing a dict to its own class attributes and vice versa converts them to dict or even a YAML string. It can also load and save data from / to file with the help of its class component BaseRepository. It gets a dict from it and converts this with its own class methods to fill the internal attributes.

### File class

This class combines the functionality of its components FileManager and FilePathGenerator. The FileManager is for certain file operations, while the FilePathGenerator can generate the needed filepaths for loading or saving, etc. The latter one comes from the principle to onle have a document (types) main folder and some kind of filename without its path and without its extension to be loaded with the help of these helper methods of the FilePathGenerator class.

### FilePathGenerator class

Serves some methods for generating correct filenames to be used for loading and saving data.

### FileManager class

This class is for basic file operations and can load and save data.

### Percentage

Basically is just a Quantity class, yet internally it will use the `self.value` divided by 100 for the `get_value()` method, which is used for math operations in the Quantity class magic methods.

### Posting class

This class shall represent a single posting on an invoice or quote. It has special classes as component and certain math operations to be executed on demand.

### PostinsList class _[TODO]_

Is supposed to hold a list of Posting class objects and serve some methods for calculation of the entries, e.g. calculating the total of all postings or similar.

### Price

Basically a Quantity class, yet for naminv convenience wrapping the class and adding some further methods, to set e.g. currency, which will just change the suffix, for example.

### Quantity class

With this class I want to have an object, which can handle quantity strings like "1.0", "1,0" or even things like "1:45 min". It will be able to parse such strings to an internal Decimal object so that math operations with this object type are possible.

### Script class _[TODO]_

This class simply is for loading and executing user scripts.

### Template class _[TODO]_

This class simply is for creatign or maybe managing templates for the rendering process.

## View

These views try to handle all input and output for / from the user.

### Printing class

Handles the basic output of printing text to the terminal.

### Render class

Handles the funcionality of rendering data to a PDF.

## Controller

These controller try to be the bridge between the View and the Model.

### commands

The click commands for the CLI interaction.

## Utils

There are certain helper utilities in this folder.

### date_utils

Certain helper methods / functions for date related things.

### file_utils

Certain helper methods, combining view elements with the File class operations.

### math_utils

Certain helper methods for cooking delicious meals ... what did you think? ;D It should be obvious that here are math related helper methods, after all. Nothing to cook, sorry.

### parsers

Certain helper methods for e.g. parsing things like "1:45 min" to proper math usable values like "1.75".
