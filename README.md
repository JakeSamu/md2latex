# README

## Minimum requirements for LaTeX
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

## Things that do not work
- Pictures that are clickable links.
    - Example code: ```[![CI](https://github.com/mame/quine-relay/workflows/CI/badge.svg)](https://github.com/mame/quine-relay/actions?query=workflow%2ACI)```
- Inlinecode - currently only standalone codeblocks, meaning that "```" is the start of a line.