'''
Creating invoices and quotes with a plaintext mindset.

Author: Manuel Senfft (www.tagirijus.de)



The core concept of the program
=== === === === === === === ===

Since the README.md should contain all needed information on how to use this
program (or even the -h/--help argument should be useful), I wanted to use
this doc string here as an explanation on how I meant the code structure to
be. It is also some kind of memory help for myself, since there is indeed some
kind if paradox: I tried very very VERY hard to make this code follow all code
conventions I know and follow a clear concept of code structure. Yet I am just
a non-professional developer to date and do not have much experience. Thus I
probably did many things different than a good professional developer would
have done. So bla bla, just let me start:


The main idea of the program, thus the code structure as well, is to have
documents to be worked with. These documents should have their own folder
(relative folders should be possible as well - not tested yet, though). With
this and their name, the idea is to have some automatic loading and saving -
without the need to specify an absolute filepath. With this base principle
I also try to have some kind of automatic list getter, which should be able
to e.g. load all documents of a certein document type and list them. This
can become handy, when e.g. calculating certain things from invoices.

So in a nutshell:

- This program is for creating (and rendering) documents.
- Documents can be of any type, which the user can create.
- The base storing file format is YAML for almost every kind of data.



The code structure
=== === === === ===

As already written above: I tried REALYL hard to make this code be easy
to understand, very well structured, modular and extendible - even in the
future, hopefully. Yet as more I tried to refactor (even when the program
was not even finished ... pre-mature, I know) ths program to become even
more dynamic, flexible, better structured and easier to understand, I fear
that I might have messed up a bit. I fear that the code is unnecessary
complicated and bloated, despite the fact that on the ground it's basically
just about rendering a YAML to PDF.

Yes, on the core it's basically just that:

                            RENDER A YAML TO PDF


ANYway: I came up with this code structure and data structure:

The core concept tries to follow the MVC principle:

                          Model + View + Controller

Thus I came up with the following strucutre. And I might have forgote something
or maybe not mention it, because it was not final. Also I might forget
something in the future, in case I extend the program yet forget about adding
new objects or so here.


###
### ### ###   Model
###

These models try to implement the core logic of the program.


BaseModel class:
    This object is the parent of the Document and the DocumentType class. It
    combines the logic of parsing a dict to its own class attributes and
    vice versa converts them to dict or even a YAML string. It can also
    load and save data from / to file with the help of its class component
    BaseRepository. It gets a dict from it and converts this with its own
    class methods to fill the internal attributes.

BaseRepository class:
    This class is meant to be a component of the BaseModel class. It is for
    file operations like saving and loading data from it and returning it
    as a dict, for example. This then can be used to by the Base class to
    fill its own class attributes, thus being "loaded".
    Itself uses the File class as a component for file operations. Also
    the automatic full filepath generation is done there.

Client class:
    Basically is a Docuemnt class, yet with a hard-coded DocumentType. I wanted
    it to be restrictive rather than the user to have it created as a new
    document type. Also for internal coherence and logic: a client can have
    certain types of documents attached to it, e.g. invoices or quotes. Maybe
    this could be done with linking documents to each other, yet I just wanted
    to have this special type of data set (the client) be a bit more pre-built.
    Again: the Client Class inherits from the Document Class.


Document class:
    This is a class, which represents any kind of document. It has DocumentType
    as a class component. This component holds the folder and the pre-built
    data types, which would nbe stored into YAML even with an "empty" data set.
    This way empty pre-filled "null-values" would be readabel in the YAML as
    well and the user would know what kind of data are needed for a specific
    kind of document type.

DocumentType class:
    Basically describes the Document class. See above.

File class:
    This class combines the functionality of its components FileManager and
    FilePathGenerator. The FileManager is for certain file operations, while
    the FilePathGenerator can generate the needed filepaths for loading
    or saving, etc. The latter one comes from the principle to onle have
    a document (types) main folder and some kind of filename without its
    path and without its extension to be loaded with the help of these
    helper methods of the FilePathGenerator class.

FilePathGenerator class:
    Serves some methods for generating correct filenames to be used for loading
    and saving data.

FileManager class:
    This class is for basic file operations and can load and save data.

Posting class:
    TODO
    Is supposed to be a single posting of the PostingList class. Has certain
    basic math operations, used for calculations inside an invoice.

PostinsList class:
    TODO
    Is supposed to hold a list of Posting class objects and serve some methods
    for calculation of the entries, e.g. calculating the total of all postings
    or similar.

Script class:
    TODO
    This class simply is for loading and executing user scripts.

Template class:
    TODO
    This class simply is for creatign or maybe managing templates for the
    rendering process.



###
### ### ###   View
###

These views try to handle all input and output for / from the user.


Printing class:
    Handles the basic output of printing text to the terminal.

Render class:
    Handles the funcionality of rendering data to a PDF.




###
### ### ###   Controller
###

These controller try to be the bridge between the View and the Model.


commands:
    The click commands for the CLI interaction.



###
### ### ###   Utils
###

There are certain helper utilities in this folder.


date_utils:
    Certain helper methods / functions for date related things.

file_utils:
    Certain helper methods, combining view elements with the File class
    operations.

math_utils:
    Certain helper methods for cooking delicious ... nah, just kidding.
    It should be obvious that here are math related helper methods.

parsers:
    Certain helper methods for e.g. parsing things like "1:45 min" to
    proper math usable values like "1.75".

'''

from plainvoice.controller.commands import cli


if __name__ == '__main__':
    cli(prog_name="plainvoice")
