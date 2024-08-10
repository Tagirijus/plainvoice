def is_convertible_to_int(string):
    '''
    Checks, if the given string can be converted into an integer.
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False
