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
- graphicx and float for inserting pictures
- verbatim for codeblocks

As long as you do not have either of those in your markdown files, you do not need the corresponding packages in LaTeX.

The following code is an example for a minimal working LaTeX-document.

```
\documentclass[a4paper, 12pt]{scrreprt}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{float}
\usepackage{verbatim}

\begin{document}
\input{example.tex}
\end{document}
```

## Important notes
### Including pictures
Since LaTeX needs to know the exact path to the file and may not have the same relative path, there are two options:
1. Always use the full path from root directory for the images.
2. Set `\graphicspath{{path/to/markdown-files/}{second/path/}}` for the files where you use relative paths to pictures.

### References
Since one might be interested in referencing specific pictures and/or sections in the final pdf, there are some rules that need to be considered.
1. Every title used in all files combined has to be unique.
2. The script cannot reference to a file directly, only to the highest title. Therefore only use full paths from root if you want to reference to a file and not a title in markdown (it needs to read the file for name of the first title).
3. Every picture gets the same reference as its name
    - so be careful if you use the same picture several times, you should probably duplicate it for reference purpose only.
4. If you want to reference something that is not possible with standard markdown, then you can use latex-reference directly via "\ref{reference-to-latex-label}".
    - For this you need to understand how the labels are automatically set. They all have the following format for titles `titlename` and for images `picturename.picturetype`.
    - Since markdown does not like empty spaces in names, we replace spaces with "-".
    - Since LaTeX does not like specific characters like "#" and "_" inside of labels, we remove all those specific characters.
    - Examples:
        - file is "test1.md" and has `# chapter 1` in it. Then you can reference via `\ref{chapter-1}`.
        - file is "test1.md" and has a picture named "screen.png" via `[screen](images/screen.png)` inserted. Then you can reference via `\ref{screen.png}`.


### Things that do not work (yet)
- Pictures that are clickable links do not work correctly. The result is a clickable caption (or more precise, figure, which is not the picture).
    - Example code: ```[![CI](https://github.com/mame/quine-relay/workflows/CI/badge.svg)](https://github.com/mame/quine-relay/actions?query=workflow%2ACI)```