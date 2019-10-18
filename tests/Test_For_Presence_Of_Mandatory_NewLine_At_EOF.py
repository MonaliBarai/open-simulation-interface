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

            # Test to check last line of file must end with a new line.
        if hasNewLine == False:
            print(file + " has no new line at the end of the file.")
            state = 1

sys.exit(state)

