#!/usr/bin/env nix-shell
#!nix-shell -i python3

# Generate a list of confusable characters from the Unicode database.
# grep 'LATIN \(SMALL\|CAPITAL\)' confusables.txt  | grep '^[0-9A-F]*[[:space:]];[[:space:]]*[0-9A-F]*[[:space:]]*;' > confusables-latin.txt

# load the confusables-latin.txt file into a dictionary
confusables = {}
black_list = [
        'CHEROKEE'
        'COPTIC',
        'ELBASAN',
        'TELUGU',
        'KANNADA',
        'MALAYALAM',
        'SINHALA',
        'DEVANAGARI'
        'GURMUKHI',
        'GUJARATI',
        'WARANG CITI',
        'WITHOUT HANDLE',
        'FULLWIDTH',
        'DESERET',
        'LOOP',
        'SHORT RIGHT LEG',
        'BLACKLETTER',
        ]

white_list = [
        'MATHEMATICAL',
        'GREEK',
        'CYRILLIC',
        ]

import re

with open('confusables-latin.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue

        # only include lines that have both a and b in the white list
        # use regular expressions to match the white list
        if not any([re.search(w, line) for w in white_list]):
            continue

        # if the line matches any of the ignore classes, skip it
        # if any([c in line for c in black_list]):
        #    continue


        line = line.strip()
        if not line:
            continue
        # print(line)
        a, b, _ = line.split(';')
        a = a.strip()
        b = b.strip()

        confusables[a] = b

reverse_confusables = {}
for a, b in confusables.items():
    # the reverse stores a list
    if b not in reverse_confusables:
        reverse_confusables[b] = []
    reverse_confusables[b].append(a)

def get_confusables(c):
    """ Given a character, return a list of confusable characters.
    look in confusable and reverse_confusables """

    # get the unicode code point for the character padded to 4 digits
    unicode_code_string = hex(ord(c))[2:].upper().zfill(4)

    forward_confusables = [] if unicode_code_string not in confusables else [confusables[unicode_code_string]]

    backward_confusables = reverse_confusables.get(unicode_code_string, [])

    return forward_confusables + backward_confusables

import random
def make_silly(string):
    """
    Given a string replace each character with a random confusable character.
    """
    output = ''
    for c in string:
        confusables = get_confusables(c)
        if confusables:
            random_replace = random.choice(confusables)
            replacemente_char = chr(int(random_replace, 16))
            output += replacemente_char
        else:
            output += c
    return output

if __name__ == '__main__':
    # read from stdin
    import sys
    for line in sys.stdin:
        print(make_silly(line), end='')
