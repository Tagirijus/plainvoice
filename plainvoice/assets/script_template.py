from plainvoice import Document
from plainvoice import Config


config: Config = config  # type: ignore
data: Document = data  # type: ignore


print('You can use "data" as the DataModel object inside your scripts:')

if data.is_visible():
    print('  -> data is visible')
else:
    print('  -> data is hidden')

print()

print('You can also use "config" as the config object in your scripts:')
print(f'  -> the text editor to use is: {config.get("editor")}')

print('And you can also use "user" as the user object in your scripts')
print('Read the "user_" related config points in the config doc strings.')
