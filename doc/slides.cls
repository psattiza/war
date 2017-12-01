\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{slides}[2017/09/05]

\LoadClass[mathserif,aspectratio=1610]{beamer}
\usetheme{Luebeck}
\usecolortheme{beaver}
\definecolor{csblue}{RGB}{33,49,77}
\definecolor{csred}{HTML}{D2492A}
\definecolor{csgrey}{HTML}{D9D9D9}
\setbeamercolor{titlelike}{fg=csblue}

\setbeamertemplate{headline}{}

\setbeamertemplate{footline}{%
\leavevmode%
\resizebox{\paperwidth}{!}{%
\colorbox{csblue}{\makebox[0.1\paperwidth]{}}%
\colorbox{csred}{\makebox[0.9\paperwidth]{}}}
\resizebox{\paperwidth}{!}{%
\colorbox{csgrey}{\begin{minipage}{0.5\paperwidth}
\includegraphics[height=0.45cm]{graphics/war}
\end{minipage}\begin{minipage}{0.5\paperwidth}
\flushright\includegraphics[height=0.45cm]{graphics/csmines}
\end{minipage}}}%
\vskip0pt%
}

\RequirePackage{graphicx}

\RequirePackage{ifxetex}
\ifxetex\RequirePackage{fontspec}\fi

\RequirePackage{minted}
\RequirePackage{xcolor}
\setminted{autogobble,python3,mathescape}
\usemintedstyle{emacs}

\RequirePackage{tcolorbox}

\RequirePackage[overlay,absolute]{textpos}

\beamertemplatenavigationsymbolsempty%

\newcommand\mi[1]{\mintinline{python3}{#1}}

\date{}

\AtBeginDocument{%
    {%
        \setbeamertemplate{footline}{}
        \setbeamertemplate{headline}{}
        \begin{frame}
            \begin{textblock*}{6pt}(0pt,0pt)
                \resizebox{\paperwidth}{!}{%
                \colorbox{csred}{\makebox[0.1\paperwidth]{}}%
                \colorbox{csgrey}{\makebox[0.9\paperwidth]{}}}
            \end{textblock*}
            \begin{center}
                \huge
                \inserttitle
            \end{center}
            \begin{center}
                \large
                \insertsubtitle
            \end{center}
        \end{frame}
    }
}
