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


            #Test to check if more than two forward slash('/') are present in comment section of proto file.
            if line.find("///") != -1:
                print(file + " in line " + str(i) + ": not permitted use of '///' ")
                state = 1

                # --------------------------------------------------------------
                #Test to check if comments are given using invalid syntax '/*'
            if line.find("/*") != -1:
                print(file + " in line " + str(i) + ": not permitted use of '/*' ")
                state = 1

                # --------------------------------------------------------------
                # Test to check if comments are given using invalid syntax '*/'
            if line.find("*/") != -1:
                print(file + " in line " + str(i) + ": not permitted use of '*/' ")
                state = 1

sys.exit(state)