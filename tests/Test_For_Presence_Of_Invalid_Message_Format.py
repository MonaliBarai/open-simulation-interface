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

            # --------------------------------------------------------------
            # Tthis section will check message name, field type and field name.
            # Check (nested) messages

            if isEnum is False:
                # Check if not inside an enum.

                # Search for "message".
                matchMessage = re.search(r"\bmessage\b", statement)
                if matchMessage is not None:
                    # a new message or a new nested message
                    noMessage += 1
                    endOfLine = statement[matchMessage.end():]
                    matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                    if matchName is not None:
                        # Test to check if message name have any special character. It should not have any special character.
                        # Message should always start with special character.
                        matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])
                        if matchNameConv is None:
                            print(file + " in line " + str(i) + ": message name wrong. '" + endOfLine[matchName.start():matchName.end()] + "'")
                            state = 1
                elif re.search(r"\bextend\b", statement) is not None:
                    # treat extend as message
                    noMessage += 1
                else:
                    # Check field names
                    if noMessage > 0:
                        matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                        if matchName is not None:
                            checkName = statement[matchName.start():matchName.end() - 1]
                            #Test to check if field names are in lower case.
                            if checkName != checkName.lower():
                                print(file + " in line " + str(i) + ": field name wrong. '" + checkName + "' should use lower case")
                                state = 1
                            # Check field message type (remove field name)
                            type = statement.replace(checkName, "")
                            matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                            if matchName is not None:
                                checkType = " " + type[matchName.start():matchName.end() - 1] + " "
                                # Test to check nested message type
                                matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)
                                if matchNameConv is None:
                                    print(file + " in line " + str(i) + ": field message type wrong. Check: '" + checkType + "'")
                                    state = 1

                            if re.search(r"\boptional\b", type) is None and re.search(r"\brepeated\b",type) is None:
                                # Test to check if every field has the multiplicity "repeated" or "optional"
                                print(file + " in line " + str(i) + ": field multiplicity (\"optional\" or \"repeated\") is missing. Check: '" + statement + "'")
                                state = 1




                # Search for a closing brace.
                matchClosingBrace = re.search("}", statement)
                if noMessage > 0 and matchClosingBrace is not None:
                    noMessage -= 1

            # Search for "enum".
            matchEnum = re.search(r"\benum\b", statement)

            if matchEnum is not None:
                isEnum = True
                endOfLine = statement[matchEnum.end():]
                matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                if matchName is not None:
                    # Test to check presence of invalid special characters
                    matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",
                                              endOfLine[matchName.start():matchName.end()])
                    if matchNameConv is None:
                        print(file + " in line " + str(i) + ": enum name wrong. '" + endOfLine[
                                                                                     matchName.start():matchName.end()] + "'")
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
