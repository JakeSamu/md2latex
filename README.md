# README

This is a python package for converting markdown to latex with with easy command configuration.

## Usage

Import this into your code and then use one of the following commands:
- outstring = md2latex.string_to_string(instring)
- outstring = md2latex.file_to_string(infile)
- md2latex.string_to_file(instring, outfile)
- md2latex.file_to_file(infile, outfile)

The converted string/file is not a standalone working LaTeX project. The result is what you need to insert inside the document environment on your own.

## Python Requirements
Python 3!

Only re is used, so no real dependencies are used and therefore no requirements.txt exists.

## LaTeX Requirements
You need to use some latex packages for different features of markdown.
- hyperref package for links
- tabularx for tables
- graphicx and float for inserting pictures
- verbatim for codeblocks

As long as you do not have either of those in your markdown files, you do not need the corresponding packages in LaTeX.

The following code is an example for a minimal working LaTeX-document.

```
\documentclass[a4paper, 12pt]{scrreprt}
\usepackage{hyperref}
\usepackage{tabularx}
\usepackage{graphicx}
\usepackage{float}
\usepackage{verbatim}

\begin{document}
\input{example.tex}
\end{document}
```

# Error
## Things that do not work (yet)
- Pictures that are clickable links do not work correctly. The result is a clickable caption (or more precise, figure, which is not the picture).
    - Example code: ```[![CI](https://github.com/mame/quine-relay/workflows/CI/badge.svg)](https://github.com/mame/quine-relay/actions?query=workflow%2ACI)```