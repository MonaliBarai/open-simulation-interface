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

            # Test to check if '\\brief' is appended in comment section for short comments.
            if matchComment is not None:
                noComment += 1;
                if comment.find("\\brief") != -1:
                    hasBrief = True;
            elif len(saveStatement) == 0:
                    # Test to check if short comment is of minimum two lines.
                    if noComment == 1:
                        print(file + " in line " + str(i - 1) + ": short comment - min. 2 lines.")
                        state = 1
                    if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b",statement) is not None:
                        if hasBrief == False:
                            # Test to check message and extend has \brief comment.
                            print(file + " in line " + str(i - 1) + ": \\brief section in comment is missing for: '" + statement + "'")
                            state = 1
                    elif hasBrief == True:
                        # Test to check if unnecessary '\brief' is mentioned for comments other than message and extend.
                        print(file + " in line " + str(i - 1) + ": \\brief section in comment is not necessary for: '" + statement + "'")
                        state = 1

                    if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b",statement) is not None or re.search(r"\benum\b", statement) is not None:
                        if noComment == 0:
                            # Test to check if every message, extend or enum has a comment
                            print(file + " in line " + str(i) + ": comment is missing for: '" + statement + "'")
                            state = 1

                    if noMessage > 0 or isEnum == True:
                        if statement.find(";") != -1:
                            if noComment == 0:
                            # Test to check if every statement has comment.
                                print(file + " in line " + str(i) + ": comment is missing for: '" + statement + "'")
                                state = 1

                    noComment = 0
                    hasBrief = False

sys.exit(state)

