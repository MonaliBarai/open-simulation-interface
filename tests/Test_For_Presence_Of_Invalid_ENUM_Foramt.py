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

            # Divide statement and comment. Concatenate multi line statements.

            # Search for comment ("//").
            matchComment = re.search("//", line)

            if matchComment is not None:
                statement = line[:matchComment.start()]
                comment = line[matchComment.end():]
            else:
                statement = line
                comment = ""

            # Add part of the statement from last line.
            statement = saveStatement + " " + statement
            saveStatement = ""

            # New line is not necessary. Remove for a better output.
            statement = statement.replace("\n", "")
            comment = comment.replace("\n", "")

            # Is statement complete
            matchSep = re.search(r"[{};]", statement)
            if matchSep is None:
                saveStatement = statement
                statement = ""
            else:
                saveStatement = statement[matchSep.end():]
                statement = statement[:matchSep.end()]

            # This section will check camelcase for enums and check enum name?

            if isEnum is True:
                matchName = re.search(r"\b\w[\S:]+\b", statement)
                if matchName is not None:
                    checkName = statement[matchName.start():matchName.end()]
                    # Test to check correct ENUM name.
                    if checkName.find(enumName) != 0:
                        print(file + " in line " + str(i) + ": enum type wrong. '" + checkName + "' should start with '" + enumName + "'")
                        state = 1
                    # Test to check ENUM type is in captial letters/upper case.
                    elif checkName != checkName.upper():
                        print(file + " in line " + str(i) + ": enum type wrong. '" + checkName + "' should use upper case")
                        state = 1

            # Search for "enum".
            matchEnum = re.search(r"\benum\b", statement)

            if matchEnum is not None:
                isEnum = True
                endOfLine = statement[matchEnum.end():]
                matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                if matchName is not None:
                        # Test to ensure no special characters are in ENUM name.
                        matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                        if matchNameConv is None:
                            print(file + " in line " + str(i) + ": enum name wrong. '" + endOfLine[matchName.start():matchName.end()] + "'")
                            state = 1
                        enumName = convert(endOfLine[matchName.start():matchName.end()]) + "_"

            # Search for a closing brace.
            matchClosingBrace = re.search("}", statement)
            if isEnum is True and matchClosingBrace is not None:
                isEnum = False
                enumName = ""


            def convert(name):
                s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
                return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

sys.exit(state)