#!/usr/bin/python3

# General utility methods - collected from various sources

def utc_str():
    from datetime import datetime
    utc = datetime.utcnow()
    return utc.strftime("%s")

''' Check if a file exists and is accessible. '''
def file_accessible(filepath, mode):
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True

def filter_nonprintable(text):
    import string
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})