import sys
import unicodedata
import re
from glob import *

state = 0

for file in glob("*.*"):
    with open(file, "rt") as fin:
        i = 0
        isEnum = False
        enumName = ""
        noMessage = 0
        noComment = 0
        hasBrief = False
        hasNewLine = True
        htmlblock = False
        saveStatement = ""

        for line in fin:
            i = i + 1
            hasNewLine = line.endswith("\n")

# Test case is checking if there is an "Umlaut" or any non ASCII characters are present.
            if (sys.version_info >= (3, 0)):
                if line != unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode():
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1
            else:
                if line != unicodedata.normalize('NFKD', unicode(line, 'ISO-8859-1')).encode('ASCII', 'ignore'):
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1
sys.exit(state)