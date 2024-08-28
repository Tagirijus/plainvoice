print('You can use "data" as the DataModel object inside your scripts:')

if data.is_visible():
    print('  -> data is visible')
else:
    print('  -> data is hidden')

print()

print('You can also use "config" as the config object in your scripts:')
print(f'  -> the text editor to use is: {config.get("editor")}')
