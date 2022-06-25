# For reading and writing files
encodingtype = "utf-8"

# This value shifts the markdown header to smaller LaTeX headers
# Value of 0 means that headers with one "#" are chapters, with "##" sections, with "###" subsections and after that just large and bold text.
# Value of 1 means, that "#" is already a section, "##" a subsection, etc.
min_title_depth = 0

# The LaTeX command that inserts a given picture is the following.
includegraphic = "\\includegraphics[width=0.9\\linewidth,height=0.6\\textheight,keepaspectratio=true]"

# The LaTeX variable given to a figure. Default is [H] for creating the picture at exactly the same place.
figurefloat = "[H]"

# Define what kind of environment latex should use for not numbered and numbered list
latextype_notnumbered = "itemize"
latextype_numbered = "enumerate"
# Define what kind of environment LaTeX should use for full codeblocks (not inline code)
codeblockenv = "verbatim"