#!/usr/bin/python3

# General utility methods - collected from various sources
import logging

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

def set_logging(setlevel):
    logging.basicConfig(level=setlevel, format='%(asctime)s %(filename)s [%(lineno)4d] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def parse_version(content):
    import re
    ver = ''
    if content != '':
        # 2 groups matching - will always return a tuple of 2 items or empty
        groups = re.findall('(\d+\.(?:\d+\.)*\d+)([\w.+-_*]+)?', content)
        if len(groups) != 0:
            # print(groups)
            part1,part2 = groups[0]
            ver = part1 + part2
            logging.info('System running FW: ' + ver)
    return ver

# Return a tuple of valid(bool),idle(float),sirq(float)
def parse_top(content):
    import re
    valid = False
    idle = 0.0
    sirq = 0.0

    matches = re.findall('(CPU:.*)', content)
    # print(matches)
    l = len(matches)
    if l == 0: return valid,idle,sirq # No match

    # Consider only the last entry
    line = matches[l-1]
    match = re.search('nic\s+(\d.*)%\s+idle', line)
    if match is not None:
        idle = float(str(match.group(1).lstrip()))
        valid = True

    match = re.search('irq\s+(\d.*)%\s+sirq', line)
    if match is not None:
        sirq = float(str(match.group(1)).lstrip())
        valid = True

    return valid,idle,sirq