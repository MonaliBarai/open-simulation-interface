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

            # Test case is checking comment and html tags
            if matchComment is not None:
                htmlComment = ""
                htmlFreeComment = comment
                if htmlblock is False:
                    matchHTMLOnly = re.search(r"\\htmlonly", comment)
                    if matchHTMLOnly is not None:

                        htmlComment = comment[matchHTMLOnly.end():]
                        htmlFreeComment = comment[:matchHTMLOnly.start()]
                        htmlblock = True
                else:
                    htmlComment = comment
                    htmlFreeComment = ""

                if htmlblock is True:
                    matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)
                    if matchEndHTMLOnly is not None:
                        htmlFreeComment = htmlFreeComment + htmlComment[matchEndHTMLOnly.end():]
                        htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                        htmlblock = False

                    # if htmlFreeComment.find("<") != -1:
                    # Test case 20 html tags only in htmlonly sections --> no error
                    # print(file + " in line " + str(i) + ": doxygen comment html tag found (use htmlonly if possible): '"+htmlFreeComment+"'")
                    ##state = 1
                if htmlComment.find("\\") != -1:
                    # Test case to check html tags only in htmlonly sections
                    print(file + " in line " + str(i) + ": doxygen comment \\.. reference found: '" + htmlComment + "'")
                    state = 1

                if htmlComment.find("#") != -1:
                    # Test case to check html tags only in htmlonly sections
                    print(file + " in line " + str(i) + ": doxygen comment #.. reference found: '" + htmlComment + "'")
                    state = 1

            elif htmlblock is True:
                # Test case 22 html tags only in htmlonly sections without end html only
                print(file + " in line " + str(i - 1) + ": doxygen comment html section without endhtmlonly")
                htmlblock = False
                state = 1

                # --------------------------------------------------------------
                # Test case 21 is checking comment and html tags
            if matchComment is not None:
                if comment.find("@") != -1:
                # Test case 21 html tags only in htmlonly sections
                    print(file + " in line " + str(i) + ": @ tag found (please replace with \\): '" + htmlFreeComment + "'")
                    state = 1
sys.exit(state)

