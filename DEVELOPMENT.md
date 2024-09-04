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

These models try to implement the core logic of the program.

### DataModel

This base model is for storing data into so called fields. There is the base attribute (at the moment only "visible" as an attribute), the additional fields and the fixed fields.

The additional fields will be filled later from the YAML (thus dict), the users fills. With that technique it is possible to have as many additional data to set by the user without coding. Yet those fields can only store basic Python types like str, int, float, list and dict.

And then there are the fixed fields as well, which need a bit more set up. They are for translating objects into a readable format and also for serving a default value. Also these fields will be always present in the data object and also later in the saved YAML file. That way it will be possible later to describe some kind of document type, which should have certain fields at least (or as a hint to the user, what to fill in that document).

### DataRepository

This object is capable of loading a DataModel by just a folder and its name. It should be used as a basis for simply loading a Document with just its type name and document name later (if no absolute filename will be given, of course).

### Document

This class is the main document object. It can be anything, due to the DocumentType class, which is able to describe the fixed fields of an instance of Document.

The idea is that the program is all about such documents in the end. That's why I tried to make them as flexible as possible. Sure it could have been handled all with just a dict, which the user could define or so. And then just take the dict to be used inside the Jinja renderer. Yet I wanted to have some kid of intuitive document handling inside the YAML file. I wanted to have such a file be structure by certain field types: base, fixed and additional. These are the main concept points of the DataModel (from which this class also is inherited).

The base fields are data related attributes. For the document it shall be the "visible" state, yet additionally also the "document_type" and (still in dev) the "links" to represent links between other DataModel objects.

Then there are the fixed fields. The concept behind them is to have fields, which are "always there", even if no value is given. Then there should be a default at least. The idea behind this is that there always shoudl be keys in the YAML for new documents so that the user knows which fields are supposed to be used for a certain document. E.g. an invoice should probably have a "date" field. Then "date" could be added as a fixed field so that for new invoices there will always be "date" as a key with a default value in the new YAML file already.

Finally there are the additional fields, which are basically just keys, which may exist in the YAML and the DataModel assigns them to the internal additional fields dict. That way a user can even have additional key+value paris on the fly to be used in the Jinja template later directly.

### DocumentLink

This class represents a single link between two documents. It can generate a unique id for this link based on the filenames of the linked documents. Also it can return the name or even the whole Document object of either of the two linked documents. Also it can be used to unconnect the documents and thus deleting the link completely.

It is used by DocumentLinkManager.

### DocumentRepository

The object, which is capable of loading and saving documents depending on their document type (name) and their name.

### DocumentLinkManager

The class, which will manage and control links between documents. It can add, remove or rename documents and links between each other.

### DocumentType

This class is for describing a Document class. The idea is that the user should be able to create own document types later and the Document class can be more flexible that way. With this class the user can describe the fixed fields or a DataModel object. Also this object holds the information about where such documents are being stored (e.g. folder).

Possible _fixed field types_ are:

- Python objects:
    - bool
    - str
    - int
        - no float, due to Decimal being available
    - dict
    - list
- date
    - internally it is a datetime object
    - readable format is 'YYYY-MM-DD'
- Decimal
    - it's the decimal.Decimal object
    - readable is a float
- Percentage
    - it's an internal Quantity child
    - readable is '0 %' for example
- Posting
    - it's an internal object
    - readable is:
        - title: str
        - detail: str
        - unit_price: Price
        - quantity: Quantity
        - vat: Percentage
        - notes: str
- PostingsList
    - it's an internal object
    - readbale is a list of Posting objects
- Price
    - it's an internal Quantity child
    - readable is '1.00 €' for example
- Quantity
    - it's an internal object
    - readable is '1:30 min' for example

### FieldTypeConverter

With this class I want be able to define a data type. The idea is to have a describing dict in a YAML later (created by the user) which will describe needed fields for a certain document type. This shall be done with pure strings, describing the data type to a given field name (basically a dict key). This describing dict can look like this:

```python
{
    'username': 'str',
    'age': 'int'
}
```

This class holds the information on how to convert to and from the YAML format.

The reason for this is: if I use a Decimal or any other class I come up with, I do not want the YAML to save this Python object into the file. For Decimals I want to keep it human readable in the YAML file; like:

    amount: 1.5

Instead of

    amount: <python.object.Decimal> ...

Or however this could look like. Thus I need some kind of converter, which will know on which field name (key) which type of data exists and how to convert it in both directions.

### FieldConversionManager

This class basically mainly just "executes", what the FieldTypeConverter describes. With this class you can set up fields for a data object later and then convert the fields to the human readable type to store in the YAML or convert it back from it.

It is also for filling missing fields. E.g. if the user did not enter some field, yet the descriptor knows this field. Then it will just added to the dict with its defined default value.

TODO: Maybe I could make the default-value-adding process optional with a class attribute. Just in case that I, at some point, to not want that "empty fields" will still be added. Yet in the human readable YAML feil later the idea is to see what kind of fields are supposed to exist for a certain document type, for example. E.g. an invoice is supposed to have a postings list.

### File

This class combines the functionality of its components FileManager and FilePathGenerator. The FileManager is for certain file operations, while the FilePathGenerator can generate the needed filepaths for loading or saving, etc. The latter one comes from the principle to onle have a document (types) main folder and some kind of filename without its path and without its extension to be loaded with the help of these helper methods of the FilePathGenerator class.

### FilePathGenerator

Serves some methods for generating correct filenames to be used for loading and saving data.

### FileManager

This class is for basic file operations and can load and save data.

### Percentage

Basically is just a Quantity class, yet internally it will use the `self.value` divided by 100 for the `get_value()` method, which is used for math operations in the Quantity class magic methods.

### Posting

This class shall represent a single posting on an invoice or quote. It has special fixed fields `title, detail, unit_price, quantity, vat` and certain math operations to be executed on demand.

### PostinsList

Is supposed to hold a list of Posting class objects and serve some methods for calculation of the entries in total.

### Price

Basically a Quantity class, yet for naminv convenience wrapping the class and adding some further methods, to set e.g. currency, which will just change the suffix, for example.

### Quantity

With this class I want to have an object, which can handle quantity strings like "1.0" or even things like "1:45 min". It will be able to parse such strings to an internal Decimal object so that math operations with this object type are possible.

### Script

This class will be instantiated with a string, which holds Python code. It then can execute this Python string and get a DataModel as argument to be passed on to the script.

### ScriptRepository

This class knows where scripts are stored and can load a script by its name and return this Script instance.

### TemplateRepository

Can create template from hard-coded template and list templates and so on.

## View

These views try to handle all input and output for / from the user.

### Printing

Handles the basic output of printing text to the terminal.

### Render

Handles the funcionality of rendering data to a PDF.

## Controller

These controller try to be the bridge between the View and the Model.

### commands

The click commands for the CLI interaction. I organized the files into _py_ scripts according to their domain:

- cli.py: The basic and main commands and cli setup.
- doctype.py: Commands for the document types.
- document.py: Commands for the documents.
- script.py: Commands for the scripts.
- template.py: Commands for the templates.

To make things better readable and easier to maintain in the future, I added some kind of abstraction layers (do you even call it that way?) between the click methods and the underlying logic to execute certain class methods etc. That way I am also able to re-use certain code, which might recur. Basically every above listed command domain (except the main one) has its own `Controller` to handle the internal logic. Maybe I can even re-use such controllers in a GUI / TUI or so later as well.

The controller are named according to these click command script files. See the respective sections in the _Controller_ section accordingly named with `*Controller`.

### DocumentTypeController

Handles DocumentType managing.

### DocumentController

Handles Document managing.

### IOFacade

This helper class is for handling output and inputs. It is somehow meant to act as some kind of wrapper so that I could, e.g., replace the `rich` module with something else later, if needed, in case I had to. That way all other classes would still use this _IOService_ class for in- and output and I only had to change this class instead of all other classes.

### ScriptController

Handles Script managing.

### TemplateController

Handles Template managing.

## Utils

There are certain helper utilities in this folder.

### data_utils

At the moment there are helper for the YAML string creation so that e.g. a multline string will get converted in a specific format.

### math_utils

Certain helper methods for cooking delicious meals ... what did you think? ;D It should be obvious that here are math related helper methods, after all. Nothing to cook, sorry.
