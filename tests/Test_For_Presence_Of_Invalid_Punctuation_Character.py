import sys
import unicodedata
import re
from glob import *


state = 0

for file in glob("*.proto"):
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

# Test to check invalid punctuation character  '__'
            if line.find("__") != -1:
                print(file + " in line " + str(i) + ": not permitted use of '__' ")
                state = 1

sys.exit(state)