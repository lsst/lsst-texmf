%% ------------------------------------------------------------
%% LSST beamer class
%% ------------------------------------------------------------
%%
%% A document class based on beamer.cls copied from Gaia original from Daniel Michalik
%% 
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{lsstbeamer}[2016/12/13 v1.0
	LSST Beamer class
    ]


\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions
\LoadClass[t]{beamer}


\definecolor{LSSTcyan}{HTML}{1084C1}


\RequirePackage{ifthen}
\usepackage{url}
\usepackage{longtable}
%\usetheme{Boadilla}
\usetheme{Rochester}

\usepackage{natbib}

\usepackage{array}


\usepackage{tikz,hyperref,amsmath}
\usetikzlibrary{positioning,arrows,shapes,decorations.shapes,shapes.arrows}
\usetikzlibrary{backgrounds,calc,decorations.pathreplacing}

\newcommand{\tikzmark}[1]{\tikz[overlay,remember picture] \node (#1) {};}

%define right justified column with custom width
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}


\newdimen\myleftmargin
\newdimen\myrightmargin
\newdimen\footrightmargin

\setlength\myleftmargin{0.3cm}
\setlength\myrightmargin{0.3cm}

\setlength\footrightmargin{0.1cm}

\mode<presentation>

\setbeamersize{sidebar width left=0cm}
\setbeamersize{text margin left=\myleftmargin}
\setbeamersize{sidebar width right=0cm}
\setbeamersize{text margin right=\myrightmargin}

\useinnertheme{circles}
  \usefonttheme[onlymath]{serif}
  \setbeamercovered{transparent}
  \setbeamertemplate{blocks}[rounded][shadow=true]
  \setbeamercolor{palette primary}{fg=white,bg=LSSTcyan}
  \setbeamercolor{palette secondary}{fg=black,bg=LSSTcyan}
  \setbeamercolor{palette tertiary}{bg=white}
  \setbeamercolor{palette quaternary}{bg=white}
  \setbeamercolor{palette sidebar primary}{fg=white,bg=LSSTcyan}
  \setbeamercolor{palette sidebar secondary}{fg=white,bg=LSSTcyan}
  \setbeamercolor{palette sidebar tertiary}{fg=white,bg=LSSTcyan}
  \setbeamercolor{palette sidebar quaternary}{fg=white,bg=LSSTcyan}

  \setbeamercolor*{author in head/foot}{fg=gray,bg=white}  
  \setbeamerfont{author in head/foot}{series=\normalfont,size=\fontsize{6}{6}}
  
  \setbeamercolor{title in head/foot}{fg=gray,bg=white}
  \setbeamerfont{title in head/foot}{series=\normalfont,size=\fontsize{6}{6}}
  
  \setbeamercolor{page number in head/foot}{fg=gray,bg=white}
  \setbeamerfont{page number in head/foot}{series=\normalfont,size=\fontsize{6}{6}}
  
  \setbeamercolor{frame title}{fg=white,bg=LSSTcyan}
  \setbeamercolor{block title}{fg=white,bg=LSSTcyan}
  \setbeamercolor{itemize item}{fg=LSSTcyan}


% This lists some useful things I didn't use but you that might be in general required
% - Add a graphic on the title page: \titlegraphic{\includegraphics{logo}}
% - Include a logo placed by your theme: \logo{\includegraphics[height=0.5cm]{logo}}
% - Embed movies into your slides
%	Note that the file needs to be on your computer, it will NOT be included in the PDF
%	This will not work with all pdf viewers - test before you're going to present this
%	\usepackage{multimedia}
%	\movie[height=5cm,width=6.5cm,loop]{}{move.avi}

% Makes overlays that are not (yet/any more) displayed transparent
\setbeamercovered{transparent}

%\setbeamertemplate{navigation symbols}{} % uncomment if you don't like the nav symbols



\newcommand{\setLogoleft}[1]{\def\@logoleft{#1}} \setLogoleft{}

\providecommand\primarycolor{blue}

% Defines the key color of the theme. 
\setbeamercolor{structure}{fg=\primarycolor}

% If insertframetitle doesn't exist, print something empty.
\providecommand\insertframetitle{} 

\setbeamertemplate{frametitle}[default][center]
\setbeamercolor*{frametitle}{fg=white,bg=}
\addtobeamertemplate{frametitle}{\vspace*{-1.05cm}}{\vspace*{0.17cm}}
\setbeamertemplate{headline}{
  \vspace*{-1ex}
 
  \leavevmode%
  \hspace*{-4pt} \hbox{%
  \begin{tikzpicture}[background rectangle/.style={fill=LSSTcyan}, show background rectangle]
 \node (logo) at (0,0){\includegraphics[height=0.7cm]{lsst_logo_notext}};
	\node (title) [right=of logo, text width=\textwidth-5.8cm]{};
    \node (scope) [right= of title ] {\includegraphics[height=0.7cm]{lsstscope}};
	\node (fill) [right=of scope, text width=.2cm]{};
    \end{tikzpicture}
  }
}

\mode<all>


  
\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
  \begin{beamercolorbox}[wd=.7\paperwidth,ht=2.25ex,dp=1ex,left]{title in head/foot}%
    \usebeamerfont{title in head/foot}\hspace*{.005\paperwidth}\insertshorttitle \hspace*{.005\paperwidth}\textbar\hspace*{.005\paperwidth}%
    \usebeamerfont{author in head/foot}\insertshortauthor \hspace*{.01\paperwidth}\textbar\hspace*{.005\paperwidth} %
    \usebeamerfont{date in head/foot}\insertshortdate \hspace*{.01\paperwidth}\textbar\hspace*{.005\paperwidth} %
    \usebeamerfont{page number in head/foot}\insertframenumber{}/\inserttotalframenumber
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.3\paperwidth,ht=2.25ex,dp=1ex,right]{page number in head/foot}%
    \usebeamerfont{page number in head/foot}Large Synoptic Survey Telescope \hspace*{.005\paperwidth}
  \end{beamercolorbox}%
  }
}

\newenvironment{agaframe}[2][1]{%
\begin{frame}[#1]
  \frametitle{#2}
  \hypertarget<1>{\insertframetitle}{}
  \only<1>{\pdfbookmark[2]{\insertframetitle}{\insertframetitle}}}%
{\end{frame}}

%
% First argument is number of frames, second is frame-title, third argument is
% the text for the PDF bookmark. The latter is useful if the title contains
% latex math which does not work in the PDF bookmarks.
%
\newenvironment{agaframealt}[3][1]{%
\begin{frame}[#1]
  \frametitle{#2}
  \hypertarget<1>{\insertframetitle}{}
  \only<1>{\pdfbookmark[2]{#3}{#3}}}%
{\end{frame}}


\def\aaps{A\&AS}           % Astronomy and Astrophysics Suplement
\def\aap{A\&A}             % Astronomy and Astrophysics
\def\ssr{Space~Sci.~Rev.}  % Space Science Reviews
\def\apj{ApJ}              % Astrophysical Journal
\def\aj{AJ}                % Astronomical Journal
\def\mnras{MNRAS}          % Monthly Notices of the RAS
\def\araa{ARA\&A}          % Annual Review of Astron and Astrophys
\def\nat{Nature}           % Nature
\def\apjl{ApJ}             % Astrophysical Journal, Letters

\def\degr{\hbox{$^\circ$}} 
\def\arcmin{\hbox{$^\prime$}}
\def\arcsec{\hbox{$^{\prime\prime}$}}
\def\fs{\hbox{$.\!\!^{\rm s}$}}
\def\fdg{\hbox{$.\!\!^\circ$}}
\def\farcm{\hbox{$.\mkern-4mu^\prime$}}
\def\farcs{\hbox{$.\!\!^{\prime\prime}$}}
\def\sun{\hbox{$\odot$}}


\newcommand{\bfvec}[1]{\mbox{$\bf#1$}}
\newcommand{\citell}{\citeyear}
\newcommand{\citellp}{\citeyearpar}
%\newcommand*{\newblock}{}
%% 
%% End of file `gaiasocbeamer.cls'.
