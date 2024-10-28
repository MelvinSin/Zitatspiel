\NeedsTeXFormat{LaTeX2e}


\LoadClass[a4paper,11pt]{article}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
%%%%% packages
\usepackage{geometry}
\geometry{a4paper,left=30mm,right=30mm, top=3cm, bottom=3cm}

\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
% \usepackage[ngerman]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{float}
\usepackage{enumerate}
\usepackage{newalg}
\usepackage{comment}
\usepackage[pdfpagelabels=true,linktocpage]{hyperref}

\usepackage{tikz}
\usetikzlibrary{arrows,decorations.pathmorphing,positioning,fit,trees,shapes}

\usepackage{MnSymbol}
\usepackage{listings}
\lstset{language=C++}

%%%%% theorem environments
\newtheorem{definition}{Definition}[section]
\newtheorem{proof}{Proof}[section]
\newtheorem{Algorithm}{Algorithm}
\newtheorem{prop}{Proposition}[section]
\newtheorem{coro}{Corollary}[section]
%%%%% Float styling
\floatstyle{ruled}
\newfloat{Algorithm}{thp}{lop}
\floatname{Algorithm}{Algorithm}
\restylefloat{table}

\usetikzlibrary{positioning}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{decorations.markings}
\usetikzlibrary{automata, positioning, arrows}

\tikzset{
    graph node/.style = {
        draw,
        thick
    },
    labelled node/.style = {
        graph node,
        execute at begin node = {\strut},
        execute at end node = {\strut}
    },
    round node/.style = {
        labelled node,
        shape = circle,
        inner sep = 1pt,
        minimum size = 9mm
    },
    rounded node/.style = {
        labelled node,
        shape = rectangle,
        rounded corners = 4mm,
        inner ysep = 1pt,
        inner xsep = 5pt,
        minimum size = 9mm
    },
    ABA node/.style = {
        round node,
        font = {\large}
    },
    graph edge/.style = {
        draw,
        thick,
        shorten < = 1pt,
        shorten > = 1pt,
        > = {Latex[round, length = 2mm, width = 2mm]}
    }
}