import re
from config import *

### todo ###
def todo():
    print("""
    - Change the latexcommands to a separate config file
    - for package creation: https://python-poetry.org/
    """)
    return True



markdownspecials = ["\\","*","_","#","~","{","}","!","(",")"] # those characters can be escaped in markdown, which we need to consider for situations like \_ and unescape something like \(
latexuses = ["\\","{","}"] # those are special characters that it uses by itself. therefore these have to be escaped beforehand
latexspecials = ["#","~","_","%"] # those characters cannot be escaped beforehand, since they are used for markdown syntax. some could be done beforehand like "%", but well, let's do that last
latexdelimiters = ["|", "*", "_", "#", "!", "+", "-", "§", "/", "?", "@"]

def latex_unescape_markdownspecials(text):
    newtext = text
    for specialchar in markdownspecials:
        if specialchar not in latexuses+latexspecials:
            newtext = newtext.replace("\\"+specialchar, specialchar)
    return newtext
def latex_escape_specialcharacters_pre(text):
    # always check for \ first, otherwise it will result in problems due to changing \# to \\# and stuff like that!
    newtext = latex_unescape_markdownspecials(text)
    
    # the char \ has to be considered differently
    # first check that no \ precedes it, since then it is an escaped backslash in both markdown and latex
    # then we need to check if some special character in markdown follows after that \ ... this will be escaped for latex anyway
    # and finally grab the character that follows this, since we know then that this \ has to be escaped
    regexstring = r'(?<!\\)(?!\\).{1}\\(?![\\'
    for x in markdownspecials:
        regexstring += x
    regexstring += r'])(?!\\).{1}'

    matches = re.findall(regexstring, newtext)
    for match in set(matches):
        newtext = newtext.replace(match, match[0]+"\\"+match[1:])
    
    # all special chars besides \
    for specialchar in latexuses:
        if specialchar == "\\": continue
        newtext = newtext.replace("\\"+specialchar, specialchar)
        newtext = newtext.replace(specialchar, "\\"+specialchar)
    newtext = newtext.replace("\\\\","{\\textbackslash}")
    return newtext
def latex_escape_specialcharacters_post(text):
    newtext = text
    for specialchar in latexspecials:
        newtext = newtext.replace("\\"+specialchar, specialchar)
        newtext = newtext.replace(specialchar, "\\"+specialchar)
    return newtext



def string_to_string(instring):
    return md2latex(instring)

def string_to_file(instring, outfile):
    o = open(outfile, "w", encoding=encodingtype)
    o.write(md2latex(instring))
    return True

def file_to_string(infile):
    f = open(infile, "r", encoding=encodingtype)
    outstring = f.read()
    return md2latex(outstring)

def file_to_file(infile, outfile):
    f = open(infile, "r", encoding=encodingtype)
    o = open(outfile, "w", encoding=encodingtype)
    outstring = f.read()
    o.write(md2latex(outstring))
    return True




def convertimages(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'(!\[.*\])(\(.*\))', markdownstring)
    for match in matches:
        caption = str(match[0])[2:-1]
        filepath = str(match[1])[1:-1]
        label = filepath.split("/")[-1]
        latexcommand = f"""\\begin{{figure}}{figurefloat}
\t\\centering
\t{includegraphic}{{{filepath}}}
\t\\caption{{{caption}}}
\t\\label{{{label}}}
\\end{{figure}}
        """
        convertedstring = convertedstring.replace(match[0]+match[1], latexcommand)
    return convertedstring

def convertlinks(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'(?<=\s)(\[.*\])(\(.*\/.*\))', markdownstring)
    for match in matches:
        text = str(match[0])[1:-1]
        url = str(match[1])[1:-1]
        latexcommand = f"\\href{{{url}}}{{{text}}}"
        convertedstring = convertedstring.replace(match[0]+match[1], latexcommand)
    return convertedstring

def converturls_without_path(markdownstring):
    # not used atm
    matches = re.findall(r'(?<=\s)(http:\/\/.*|https:\/\/.+)(?<!\/)', markdownstring)
    convertedstring = markdownstring
    return convertedstring

def converturls(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'(?<=\s)https?:\/\/[\S]+', markdownstring)
    for match in matches:
        latexcommand = f"\\url{{{match}}}"
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring


def converttitles(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'\n#+.+|^#+.+', markdownstring)
    for match in matches:
        depth = match.count("#") + min_title_depth
        title = " ".join(match.split(" ")[1:])
        if depth == 1:
            latexcommand = f"\n\n\\chapter{{{title}}}"
        elif depth == 2:
            latexcommand = f"\n\\section{{{title}}}"
        elif depth == 3:
            latexcommand = f"\n\\subsection{{{title}}}"
        else:
            latexcommand = f"\n{{\\textbf\Large{{{title}}}}}\n"
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring


def shiftleft(lines, depth):
    shifted = []
    for line in lines.split("\n"):
        shifted.append(line[depth:])
    return "\n".join(shifted)

def shiftright(lines, depth):
    shifted = []
    for line in lines.split("\n"):
        shifted.append(" "*depth + line)
    return "\n".join(shifted)


def latexlist(match):
    # first check if everything needs to be shifted (for recursive subindents)
    firstline = match.split("\n")[0]
    depth = len(firstline) - len(firstline.lstrip())
    if match[0] == " ":
        match = shiftleft(match, depth)
    # then go to the main part - it got way more complicated than I wanted to ...
    itemchar = match.split(" ")[0]
    if itemchar in ("*","-"):
        latextype = latextype_notnumbered
    elif itemchar[-1] == ".":
        latextype = latextype_numbered
    else:
        print("error at computing latex list")
        print(firstline)
        exit(-1)
    content = match
    indentedlist = []
    for line in match.split("\n"):
        if line.startswith(" "):
            indentedlist.append(line)
        else:
            if indentedlist != []:
                original = "\n".join(indentedlist)
                changed = latexlist("\n".join(indentedlist))
                content = content.replace(original, changed)
                indentedlist = []
            if itemchar in ("*","-"):
                content = content.replace(line, line.replace(itemchar, "\\item", 1))
            else:
                content = content.replace(line, line.replace(line.split(".")[0]+".", "\\item", 1))
    if indentedlist != []:
        original = "\n".join(indentedlist)
        changed = latexlist("\n".join(indentedlist))
        content = content.replace(original, changed)
    
    latexcommand = f"\\begin{{{latextype}}}\n{content}\n\\end{{{latextype}}}"
    return shiftright(latexcommand, depth)

def convertlists(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'\n((?:[\*\-]|\d+\.)(?=\s).*[\s\S]*?)\n(?![\d\*\-])\S', markdownstring)

    for match in matches:
        while match.endswith("\n"): match = match[:-1]
        latexcommand = latexlist(match)
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring

def convertbold(markdownstring):
    convertedstring = markdownstring
    matches = re.findall(r'(\*{2}.*\*{2}|_{2}.*_{2})', markdownstring)
    for match in matches:
        text = match[2:-2]
        latexcommand = f"\\textbf{{{text}}}"
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring

def convertitalic(markdownstring):
    convertedstring = markdownstring
    # this only works if you catch bold first!
    matches = re.findall(r'(?<!\\)(\*{1}.*(?<!\\)\*{1}|_{1}.*(?<!\\)_{1})', markdownstring)
    for match in matches:
        text = match[1:-1]
        latexcommand = f"\\textit{{{text}}}"
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring

def convertcrossed(markdownstring):
    print("not implemented")
    # you just need to copy and paste to convertbold and change the regex such that it does not capture "_" or "*" but "~" instead.

def converttables(markdownstring):
    ## todo: currently if every line starts with "|" and one with " |" this is seen as a true list for latex but not in markdown.

    convertedstring = markdownstring
    # the idea is to get the main pattern '|-|-|' , the line before and then all lines afterwards up to an | symbol with newline and not starting with | again.
    potential_matches = re.findall(r'(.*\n[\|-][:\|\- ]*\|\n[\s\S]*?[\|-])\n(?!\|)', markdownstring)
    matches = potential_matches
    for match in potential_matches:
        counter = match.split("\n")[0].count("|")
        for line in match.split("\n")[:-1]:
            if counter != line.count("|"):
                # formatting of table is wrong
                matches.remove(match)
    # now convert it to tabularx
    for match in matches:
        tablesize = "X" * (match.split("\n")[0].count("|") - 1)
        lines = []
        for line in match.split("\n"):
            if len(line) > 0:
                s = 0
                t = None
                if line.startswith("|"): s = 1
                if line.endswith("|"): t = -1
                lines.append(" & ".join(line.split("|")[s:t]))
        lines.pop(1) # since this is just the horizontal line
        content = " \\tabularnewline\n\t".join(lines).replace("\n", "\hline\n", 1) # set horizontal line via replace
        latexcommand = f"\n\\vspace{{9pt}}\n\\begin{{tabularx}}{{\\textwidth}}{{{tablesize}}}\n\t{content}\n\\end{{tabularx}}\n\\vspace{{9pt}}"
        convertedstring = convertedstring.replace(match, latexcommand)
    return convertedstring

def convertcodeblocks(markdownstring):
    convertedstring = markdownstring
    codeblocks = []
    # full codeblocks that are not inline
    matches1 = re.findall(r'(?<!.)`{3}[\s\S]*?`{3}', markdownstring)
    # tabbed in text that has empty line above and below is a codeblock too
    matches2 = re.findall(r'\n\n((?:\s+\s+|\t+)[\s\S]*?)\n\n(?=\S)', markdownstring)
    for match in matches1+matches2:
        code = match.replace("```", "")
        while code.startswith("\n"): code = code[1:]
        while code.endswith("\n"): code = code[:-1]
        latexcommand = f"\\begin{{{codeblockenv}}}\n{code}\n\\end{{{codeblockenv}}}"
        convertedstring = convertedstring.replace(match, latexcommand)
        codeblocks.append(latexcommand)
    return (convertedstring, codeblocks)

def convertinlinecode(markdownstring):
    convertedstring = markdownstring
    inlinecodes = []
    # inline code
    matches = re.findall(r'(`+)([\s\S]*?)(`+)', markdownstring)
    for match in matches:
        if match[0] == match[2]:
            delimiter = "^"
            for x in latexdelimiters:
                if x not in match[1]:
                    delimiter = x
                    break
            latexcommand = "\\verb" + delimiter + match[1] + delimiter
            convertedstring = convertedstring.replace(match[0]+match[1]+match[2], latexcommand)
            inlinecodes.append(latexcommand)
    return (convertedstring, inlinecodes)

def find_all_occurences(text, subtext, overlap):
    start = 0
    occurences = []
    while True:
        start = text.find(subtext, start)
        if start == -1:
            break
        occurences.append(start)
        if overlap == True:
            start += 1
        else:
            start += len(subtext)
    return occurences
            

def md2latex(text):
    modified_text = text

    # check for codeblocks
    (modified_text, codeblocks) = convertcodeblocks(modified_text)
    (modified_text, inlinecodes) = convertinlinecode(modified_text)

    # now split along those codeblocks and only escape special characters outside of codeblocks 
    codeblocks = list(set(codeblocks))
    inlinecodes = list(set(inlinecodes))


    # find the indices of every text element that contains code
    code_sorted_by_occurence = []
    for code in codeblocks+inlinecodes:
        for i in find_all_occurences(modified_text, code, False):
            code_sorted_by_occurence.append((i, code))
    code_sorted_by_occurence.sort()

    # now we have a list of all text elements that contain code and should not further be modified
    # now separate the text into those that do and do not contain code
    text_splitted = []
    text_to_be_splitted = modified_text
    for (index, code) in code_sorted_by_occurence:
        noncode = text_to_be_splitted.split(code)[0]
        text_splitted.append((True, noncode))
        text_splitted.append((False, code))
        # if code appears several times, we need to rejoin it for the later appearance
        text_to_be_splitted = code.join(text_to_be_splitted.split(code)[1:])
    text_splitted.append((True, text_to_be_splitted))

    # with this we can cycle through the whole text and only modify text that does not contain code
    combiner = ""
    
    for (is_noncode,textpart) in text_splitted:
        if is_noncode == True:
            noncode = textpart
            noncode = latex_escape_specialcharacters_pre(noncode)

            # check for links and urls
            noncode = converturls(noncode)
            noncode = convertlinks(noncode)

            # check for inserted pictures
            noncode = convertimages(noncode)

            # check for titles
            noncode = converttitles(noncode)

            # check for lists
            noncode = convertlists(noncode)

            # check for emphasised text
            noncode = convertbold(noncode)
            noncode = convertitalic(noncode)

            # check for tables
            noncode = converttables(noncode)

            noncode = latex_escape_specialcharacters_post(noncode)
            
            combiner += noncode
        else:
            combiner += textpart

    return combiner


def main():
    print("No standalone main exists, please use the commands presented in the README.md")
    import sys
    file_to_file(sys.argv[1], "testoutput.tex")

main()