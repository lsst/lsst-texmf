%%------------------------------------------------------------
%% General LSST  document class --- copied from Gaia by wil
%%------------------------------------------------------------
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{lsstdoc}[2016/12/12 v1.1 LSST document class]

\LoadClass[11pt,letterpaper]{article}

% Define the default stretch
\renewcommand{\baselinestretch}{1.25}

% Must load AMS packages before loading math fonts
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{bm}
\RequirePackage{amsbsy}

\usepackage{environ}
\usepackage{enumitem}

% LSST uses a sans serif font
\RequirePackage{ifxetex}
\ifxetex
  \RequirePackage{fontspec}
  \RequirePackage{xunicode}
  \defaultfontfeatures[OpenSans]
  {
  Extension = .ttf ,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-Italic,
  BoldItalicFont = *-BoldItalic,
  SmallCapsFont = CarroisGothicSC-Regular,
  }
  \defaultfontfeatures[Inconsolata]
  {
  Extension = .ttf ,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  }
  \RequirePackage[bold-style=ISO]{unicode-math}
  \setmathfont{XITSMath-Regular.otf}
  \setmainfont[Ligatures=TeX]{OpenSans}
  \setmonofont{Inconsolata}
\else
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8x]{inputenc}
  \RequirePackage[default]{opensans}
  \RequirePackage{inconsolata}
  \RequirePackage[uprightGreek]{newtxmath}
\fi

\RequirePackage[usenames,table]{xcolor}
\RequirePackage{ifthen}
\RequirePackage{calc}
\RequirePackage{array}
\RequirePackage{fancyhdr}
\RequirePackage{multirow}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{longtable}
\RequirePackage{eso-pic}
\RequirePackage{color}
\RequirePackage{setspace}
\RequirePackage{tcolorbox}
\RequirePackage{ifmtarg}

%\RequirePackage[linkcolor=blue,colorlinks=true]{hyperref}
\RequirePackage{hyperref}

% Must be loaded AFTER hyperref (page 3 of the glossaries manual)
\RequirePackage[nonumberlist,nogroupskip,toc,numberedsection=autolabel,style=index]{glossaries}

\RequirePackage{numprint}
\RequirePackage[english,iso]{isodate}
\RequirePackage{titlesec}
\RequirePackage[english]{babel}
\RequirePackage{tabularx}
\RequirePackage{comment}
\RequirePackage{xspace}
\RequirePackage{xstring}
%\RequirePackage{microtype}
\RequirePackage{listings}
%\RequirePackage{nameref}
%\RequirePackage{mathptmx} % note this messes up \vec definition... do not e add put in your doc if you want it
\RequirePackage{tocstyle}


% Standardize bibliography styling
\bibliographystyle{lsst_aa}

% Allow different colors for each component (the original LSST
% word template was not consistent) even though for Rubin Observatory
% a single value is used of RAL5018 #058b8c (5, 139, 140)
\definecolor{lsstblue}{RGB}{ 5, 139, 140}
\definecolor{lsstsect}{RGB}{ 5, 139, 140}
\definecolor{lssttitle}{RGB}{ 5, 139, 140}
\definecolor{lssthead}{RGB}{ 5, 139, 140}
\definecolor{lsstfoot}{RGB}{ 5, 139, 140}

% Switch off the onecolumn and twocolumn options
\DeclareOption{onecolumn}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}

\newif\if@isdraft
\@isdraftfalse
\DeclareOption{lsstdraft}{
    % DRAFT
    \AddToShipoutPicture{%
            \setlength{\unitlength}{0.7pt}%
        \makeatletter
            \put(\strip@pt \textwidth,\strip@pt \textheight){%
                \makebox(0,0){%
                \rotatebox{45}{%
                    \textcolor[gray]{0.95}{%
                        \fontsize{5cm}{5cm}\textsf{Draft}%
                    }}}}%
        \makeatother
    }%
    \@isdrafttrue
}

\newif\if@isobsolete
\@isobsoletefalse
\DeclareOption{obsolete}{
    % DRAFT
    \AddToShipoutPicture{%
            \setlength{\unitlength}{0.7pt}%
        \makeatletter
            \put(\strip@pt \textwidth,\strip@pt \textheight){%
                \makebox(0,0){%
                \rotatebox{45}{%
                    \textcolor[gray]{0.95}{%
                        \fontsize{5cm}{5cm}\textsf{Obsolete}%
                    }}}}%
        \makeatother
    }%
    \@isobsoletetrue
}


% Enable author year cite mode
\newif\if@authoryear
\@authoryearfalse
\DeclareOption{authoryear}{\@authoryeartrue}
\if@compatibility\else
\DeclareOption{notoc}{\@authoryearfalse}
\fi

%
% Automatically include table of contents in maketitle with the
% addtoc option.
%
\newif\if@addtoc
\@addtocfalse
\DeclareOption{toc}{\@addtoctrue}
\if@compatibility\else
\DeclareOption{notoc}{\@addtocfalse}
\fi
%Default toc depth should be here not in the title page so you can change it
\setcounter{tocdepth}{3}
%
% Define the various document types
%
\DeclareOption{CP}{
   \renewcommand{\docType}{Conference Proceeding}
}
\DeclareOption{MN}{
   \renewcommand{\docType}{Meeting Minutes}
}
\DeclareOption{PR}{
   \renewcommand{\docType}{Progress Report}
}
\DeclareOption{SP}{
   \renewcommand{\docType}{Specification}
}
\DeclareOption{TN}{
   \renewcommand{\docType}{Technical Note}
}
\DeclareOption{TR}{
   \renewcommand{\docType}{Test Report}
}
\DeclareOption{DP}{
   \renewcommand{\docType}{Development Plan}
}
\DeclareOption{DDP}{
   \renewcommand{\docType}{Data Processing Centre Development Plan}
}
\DeclareOption{SRS}{
   \renewcommand{\docType}{Software Requirement Specifications}
}
\DeclareOption{SDD}{
   \renewcommand{\docType}{Software Design Document}
}
\DeclareOption{ICD}{
   \renewcommand{\docType}{Interface Control Document}
}
\DeclareOption{SUM}{
   \renewcommand{\docType}{Software User Manual}
}
\DeclareOption{SRN}{
   \renewcommand{\docType}{Software Release Note}
}
\DeclareOption{STP}{
   \renewcommand{\docType}{System Validation and Test Plan}
}
\DeclareOption{STS}{
   \renewcommand{\docType}{Software Test Specification}
}
\DeclareOption{STR}{
   \renewcommand{\docType}{Software Test Report}
}
\DeclareOption{VTR}{
   \renewcommand{\docType}{Validation Test Report}
}
\DeclareOption{SOW}{
   \renewcommand{\docType}{Statement of Work}
}
\DeclareOption{SPAR}{
   \renewcommand{\docType}{Software Product Assurance Report}
}
\DeclareOption{PL}{
   \renewcommand{\docType}{Planning and Policy Document}
}
\DeclareOption{UG}{
   \renewcommand{\docType}{User Guide}
}
%there is only one of these probably
\DeclareOption{SSS}{
   \renewcommand{\docType}{Software System Specification}
}
%
% Define the groups
%
\DeclareOption{PST}{
   \renewcommand{\CU}{PST}
   \renewcommand{\docType}{Project Science Team}
}
\DeclareOption{DP}{
   \renewcommand{\CU}{DP}
   \renewcommand{\docType}{Data Production}
}
\DeclareOption{PF}{
   \renewcommand{\CU}{PF}
   \renewcommand{\docType}{System Performance}
}
\DeclareOption{DM}{
   \renewcommand{\CU}{DM}
   \renewcommand{\docType}{Data Management}
}
\DeclareOption{TS}{
   \renewcommand{\CU}{TS}
   \renewcommand{\docType}{Telescope \& Site}
}
\DeclareOption{SE}{
   \renewcommand{\CU}{SE}
   \renewcommand{\docType}{Systems Engineering}
}
\DeclareOption{RDO}{
   \renewcommand{\CU}{RDO}
   \renewcommand{\docType}{Rubin Directors Office}
}
\DeclareOption{PMO}{
   \renewcommand{\CU}{PMO}
   \renewcommand{\docType}{Rubin Observatory Project Office}
}
\DeclareOption{OPS}{
   \renewcommand{\CU}{OPS}
   \renewcommand{\docType}{Rubin Observatory Operations }
}



%
% default settings for the newly defined commands
%

% you own DPC, institute or funding logo for front page
\newcommand{\setDocLocalLogo}[1]{\def\@docLocalLogo{#1}}
\setDocLocalLogo{}

\newcommand{\docType}{Rubin Observatory Document}
\newcommand{\CU}{DM}

\newcommand{\DU}{}
\newcommand{\setLSSTDU}[1]{\renewcommand{\DU}{-#1}}

%
% Titlepage design and macros
%
% footer title can be empty
\newsavebox{\footerTitle}
\sbox{\footerTitle}{}

% Override standard \title to allow shorttitle
% to be given as an optional argument. If not supplied
% the long title is used as short title.
%  \title{longtitle}
%  \title[shorttitle]{longtitle}
\renewcommand{\title}[2][@shorttitle@]{
  \gdef\@title{#2}
  \ifthenelse{\equal{@shorttitle@}{#1}}
             {\def\@docShortTitle{#2}}
             {\def\@docShortTitle{#1}}
}
\title{Set the document title with $\backslash$title}
\author{Set the document author with $\backslash$author}
\newcommand{\memoto}{set the TO with {$\backslash$}setMemoto}
\newcommand{\setMemoto}[1]{\renewcommand{\memoto}{#1}}

\newcommand{\docSubtitle}{No Subtitle}
\newcommand{\setDocSubtitle}[1]{\def\@docSubtitle{#1}
  \renewcommand{\docSubtitle}{#1}
}
\setDocSubtitle{}

\newcommand{\setDocCompact}[1]{\def\@docCompact{#1}}
\setDocCompact{}
\def\@docCompact{false}

\newcommand{\docDate}{set the date with {$\backslash$}setDocDate}
\newcommand{\setDocDate}[1]{\renewcommand{\docDate}{#1}}

% allow standard \date{} to work as an alias of \setDocDate
\renewcommand{\date}[1]{\setDocDate{#1}}

\newif\if@dmccb
\@dmccbfalse
\newif\if@ccb
\@ccbfalse
\newcommand{\docRef}{set the Reference with {$\backslash$}setDocRef}
\newcommand{\setDocRef}[1]{
   \renewcommand{\docRef}{#1}
   \if@dmccb\relax\else\IfBeginWith{#1}{LDM-}{\@dmccbtrue}{}\fi
   \if@ccb\relax\else\IfBeginWith{#1}{LSE-}{\@ccbtrue}{}\fi
   \if@ccb\relax\else\IfBeginWith{#1}{LPM-}{\@ccbtrue}{}\fi
}

\newcommand{\docAuthor}{set the Author with {$\backslash$}setDocAuthor}
\newcommand{\setDocAuthor}[1]{\renewcommand{\docAuthor}{#1}}


\newcommand{\setDocCurator}[1]{\def\@docCurator{#1}}
\setDocCurator{}

\newcommand{\setDocCitationInformation}[1]{\def\@docCitationInformation{#1}}
\setDocCitationInformation{}

\newcommand{\setDocUpstreamLocation}[1]{\def\@docUpstreamLocation{#1}}
\setDocUpstreamLocation{}

\newcommand{\setDocUpstreamVersion}[1]{\def\@docUpstreamVersion{#1}}
\setDocUpstreamVersion{}

\newcommand{\docAbstract}{}
\newcommand{\setDocAbstract}[1]{\renewcommand{\docAbstract}
{\section*{Abstract}
    \ifx \@docCompact \@empty
           \vspace*{1cm}
     \else
           \relax
    \fi
    \begin{center}
    \parbox{.9\textwidth}{#1}\\
    \end{center}
    \pagebreak
}}

\newcommand{\docChangeRecord}{}
\newcommand{\setDocChangeRecord}[1]{\renewcommand{\docChangeRecord}
{
\clearpage
\begin{docHistory}
#1
\end{docHistory}
}}

% These commands are not used by LSST but are retained as no-ops for
% compatibility with earlier usage from Gaia.
\newcommand{\setDocIssue}[1]{%
\ClassWarning{lsstdoc}{For setDocIssue please use the Change Record}}

\newcommand{\setDocStatus}[1]{%
\ClassWarning{lsstdoc}{For setDocStatus use the lsstdraft option to enable draft mode. Document is released by default.}}

\newcommand{\setDocRevision}[1]{%
\ClassWarning{lsstdoc}{For setDocRevision please use the Change Record}}

\newcommand{\setDocAffil}[1]{%
\ClassWarning{lsstdoc}{setDocAffil is no longer supported}}

\newcommand{\setDocApprove}[1]{%
\ClassWarning{lsstdoc}{For setDocApprove please use the Change Record}}

\newcommand{\setDocAuthorize}[1]{%
\ClassWarning{lsstdoc}{For setDocAuthorize authorized person is implied by document series}}

% Define the control text to use based on document type
% This was in makeTitle which means make Short title caused lits of errors
\def\@controlText{}
\def\@controlFootText{}

\newcommand{\mkmemotitle}{
   \thispagestyle{empty}
   \newgeometry{top= 1cm,left=2cm,bottom=1cm, right=2cm} 
   \vspace*{-30pt}

   \includegraphics[width=4cm]{rubin_logo}
   \hfill
   \begin{minipage}{0.3\textwidth}
        \begin{flushright}
        \vspace*{-50pt}
        \large 
        950 North Cherry Avenue,
        Tucson, AZ, 85719.
        \vspace{3mm}
	\textbf{\docDate} 
	\end{flushright}
   \end{minipage}
      
   \vspace{10pt}
   \textbf {To: \memoto}\\
   \textbf {From: \@author}\\

   \textbf {Subject: \@title }\\
}

\newcommand{\mkshorttitle}{
     \begin{center}
        \color{lssttitle}
        \@title \\
        \color{black}
        \normalsize {\textbf \@author}\\
	      \docDate\\
     \end{center}
}

\renewcommand{\maketitle}{
  \hypersetup{pdftitle={\@title\ifx\@docSubtitle\@empty\else\ - \docSubtitle\fi},
  pdfauthor={\@author},
  pdfkeywords={\docRef}}

   \thispagestyle{empty}

    \AddToShipoutPicture*{%
            \setlength{\unitlength}{0.65pt}%
        \makeatletter
            \put(\strip@pt \textwidth,192){%
                \makebox(0,0){%
			\includegraphics[width=1.01\paperwidth]{rubinobs}\\
                    }}%

        \makeatother
    }%

    % Place logo on the foreground at the top with text centred underneath it
    \AddToShipoutPictureFG*{%
      \put(\LenToUnit{0.5\paperwidth},\LenToUnit{0.77\paperheight}){%
        \makebox[0pt][c]{
		\includegraphics[width=0.42\textwidth]{rubin_logo}
		}\\
      }
    }

   \setlength{\parindent}{0pt}
   \vspace*{1in}
   \begin{center}
   \begin{minipage}{1.0\textwidth}
     \begin{center}
    \color{lssttitle}
    \textsf{\LARGE \bfseries Vera C. Rubin Observatory} \\
    \vspace*{0.1cm}
    \textsf{\LARGE \bfseries \docType } \\
    \vspace*{0.5cm}
    \begin{spacing}{2}
      \textsf{\Huge \bfseries \@title} \\
        \ifx \@docSubtitle \@empty
         \relax
      \else
           \vspace*{1cm}
           \large\@docSubtitle
      \fi
    \end{spacing}
    \vspace*{2cm}

    \color{black}
    \textsf{\Large \bfseries\@author}\\
    \vspace*{0.5cm}
    \textsf{\Large \bfseries\docRef}\\
    \vspace*{0.5cm}
    \textsf{\Large \bfseries Latest Revision: \docDate}
    \end{center}
   \end{minipage}
    \end{center}
   \vspace*{1cm}

   \if@ccb
   \def\@controlText{%
   This Rubin Observatory document has been approved as a Content-Controlled Document.
   Its contents are subject to configuration control and may not be changed, altered, or their provisions waived without prior approval.
   If this document is changed or superseded, the new document will retain the Handle designation shown above.
   The control is on the most recent digital document with this Handle in the Rubin Observatory digital archive and not printed versions.
   }
   \def\@controlFootText{%
   The contents of this document are subject to configuration control and may not be changed, altered, or their provisions waived without prior approval.
   }
   \fi
   \if@dmccb
   \def\@controlText{%
   This Rubin Observatory document has been approved as a Content-Controlled Document by the Rubin Observatory DM Change Control Board.
   If this document is changed or superseded, the new document will retain the Handle designation shown above.
   The control is on the most recent digital document with this Handle in the Rubin Observatory digital archive and not printed versions.
   Additional information may be found in the corresponding DM RFC.
   }
   \def\@controlFootText{%
   The contents of this document are subject to configuration control by the Rubin Observatory DM Change Control Board.
   }
   \fi

   % For obsolete documents we never want to report that the document is approved
   \if@isobsolete
   \def\@controlText{%
   This document is obsolete, no longer part of the baseline, and carries no authority; it is preserved for historical information only.
   }
   \def\@controlFootText{%
   This document is preserved for historical information only.
   }
   \fi


   % If this is a controlled document we need to report that.
   % For draft controlled documents we splash some red text in appropriate places.
   \ifx \@controlText \@empty
     \if@isdraft
       \begin{center}
       \color{red}
       \Large
       \textbf{D R A F T}
       \end{center}
     \fi
     \if@isobsolete
       \begin{center}
       \color{red}
       \Large
       \textbf{O B S O L E T E}
       \end{center}
     \fi
   \else
     \begin{spacing}{1.5}
       \textbf{\small
       \if@isdraft
         \color{red}
         Draft Revision NOT YET Approved
         \color{black} --
       \fi
       \if@isobsolete
         \color{red}
         Obsolete Document
         \color{black} --
       \fi
       \color{black}
       \@controlText
       \if@isdraft
       -- \color{red} Draft Revision NOT YET Approved
       \fi
       \if@isobsolete
       -- \color{red} Obsolete Document
       \fi
       \color{black}
       }
     \end{spacing}
   \fi

   %\rule{\textwidth}{0.5pt} \\[0.5cm]
   \ifx \@docCompact \@empty
       \vspace*{2cm}
     \else
     \relax
    \fi
    \color{black}

    \ifx \@docCompact \@empty
           \pagebreak
     \else
     \relax
    \fi
   \pagenumbering{roman}
   \pagebreak
   \docAbstract
   \docChangeRecord

   \if@addtoc
     \usetocstyle{standard}
     \begin{spacing}{1.5}
     \tableofcontents
     \end{spacing}
     \clearpage
     \pagenumbering{arabic}
     \begin{center}
     \textsf{\LARGE \color{lssttitle} \bfseries \@title \color{black}}
     \end{center}
   \fi
}

\ProcessOptions\relax

% Decide on type of natbib citation
\if@authoryear
  \usepackage{natbib}
\else
  \usepackage[numbers]{natbib}
\fi

%
%   Document history
%
\newenvironment{docHistory}[0]{
  \newpage
  \section*{Change Record}
  \begin{small}
    % flush table to the left
    \setlength\LTleft{0pt}
    \setlength\LTright{\fill}
%   \setlength\LTpost{\fill}
   \addtocounter{table}{-1}
    \begin{longtable}{|l|p{.13\textwidth}|p{.45\textwidth}|p{.23\textwidth}|}

    \hline
\textbf{Version} & \textbf{Date} & \textbf{Description} & \textbf{Owner name} \\ \hline\hline
    \endfirsthead
    \hline
\textbf{Version} & \textbf{Date} & \textbf{Description} & \textbf{Owner name} \\ \hline\hline
    \endhead
    \multicolumn{4}{r}{\emph{Continued on next page}}
    \endfoot
    \endlastfoot
}{
\end{longtable}
\end{small}
\ifx \@docCurator \@empty
    \relax
\else
    \emph{Document curator:} \@docCurator\\
\fi
\ifx \@docUpstreamLocation \@empty
    \relax
\else
    \emph{Document source location:} \@docUpstreamLocation\\
\fi
\ifx \@docUpstreamVersion \@empty
    \relax
\else
    \emph{Version from source repository:} \@docUpstreamVersion\\
\fi
\ifx \@docCitationInformation \@empty
    \relax
\else
    \vspace*{0.2cm}\\
    \emph{Cite as:} \@docCitationInformation\\
\fi

\clearpage
%        \ifx \@docCompact \@empty
%           \pagebreak
%         \else
%         \relax
%        \fi
}

\providecommand{\addtohist}[4]{
#1 & #2 & #3 & #4 \\\hline}


%
% Issue Lists
%
\newenvironment{issueList}[0]{
\begin{longtable}{|l|p{0.8\textwidth}|}\hline \textbf{ID}&\textbf{Summary}\\\hline
}{
\end{longtable}
}

\providecommand{\addissue}[2]{
#1 & #2\\\hline}

%
% Page layout
%
% use the "showframe" option to draw margins
\usepackage{geometry}
\geometry{textheight=8.5in,
          letterpaper,
          textwidth=6.5in,
          includeall,
          lmargin=1in,
          headheight=55pt,
          headsep=2em,
          marginparwidth=60pt,
          footskip=40pt}

\setlength{\parindent}{0cm}             % No indent at start of paragraphs
\setlength{\parskip}{\baselineskip}     % Blank line between paragraph

\pagenumbering{arabic}
\mark{{}{}}

\newcommand{\clearemptydoublepage}{\newpage{\pagestyle{empty}\cleardoublepage}}

%% min page fraction that must be filled with text
\renewcommand{\textfraction}{0.1}
%% max page fraction that a float may take at the top of the page
\renewcommand{\topfraction}{0.9}
%% max page fraction that a float may take at the bottom of the page
\renewcommand{\bottomfraction}{0.9}
%% max page fraction that may be filled with floats
\renewcommand{\floatpagefraction}{0.5}
%% maximum number of floats at the top of the page
\setcounter{topnumber}{3}
%% maximum number of floats at the bottom of the page
\setcounter{bottomnumber}{1}
%% maximum total number of floats on a page
\setcounter{totalnumber}{5}

\def\fps@figure{!htbp}

\setcounter{secnumdepth}{5}    % numbering level of sections

% Header and footer definitions

\pagestyle{fancy}

% Clear all headings
\fancyhead{}


% Dynamically calculate the spacing so that it is driven solely by
% the amount of overhang required and the width of the logo.
\newlength{\lsstheadlogowidth}
\setlength{\lsstheadlogowidth}{0.18\textwidth}

% Total width of header minipage
\newlength{\lsstheadwidth}
\setlength{\lsstheadwidth}{ \textwidth}

% Text to use below the logo in the header
\newcommand{\headertext}{\tiny Vera C. Rubin Observatory}

% Calculate space taken up by the LSST header text
% \settowidth does not seem to work properly with pdflatex
\newlength{\lsstheadertextwidth}
\ifxetex
  \settowidth{\lsstheadertextwidth}{\headertext}
\else
  \setlength{\lsstheadertextwidth}{105pt}
\fi

% Additional space between rule and header LSST text
\newlength{\lsstheadergap}
\setlength{\lsstheadergap}{0.0cm}

% Length of first part of ruler depends on text being centred below the logo.
\newlength{\lsstleftheadrule}
\setlength{\lsstleftheadrule}{ 0.5\lsstheadlogowidth -
                              0.5\lsstheadertextwidth - \lsstheadergap}

% Define command to fill the rest of the line with a rule of specified thickness
\def\vhrulefill#1{\leavevmode\leaders\hrule\@height#1\hfill \kern\z@}

% Left heading is the logo and horizontal rule
\lhead{%
\vspace {-10pt}
\includegraphics[width=\lsstheadlogowidth]{rubin_logo}\\
}

% Right heading is the document description.
\rhead{%
\begin{minipage}{13.3cm}
  \vspace {-2.8cm}
  \tiny
  \color{lssthead}
  \sffamily
  \textbf{\hfill \@docShortTitle ~|~\docRef ~|~ Latest Revision \docDate}
\end{minipage}%
}

\renewcommand{\headrulewidth}{0.0pt}

\renewcommand{\footrulewidth}{1pt}

% If this is not a controlled document we have space for DRAFT in the left and right footer
\newcommand{\@draftFooterText}{
\ifx \@controlText \@empty
  \if@isdraft
    \color{red}\textbf{D R A F T}
  \fi
  \if@isobsolete
    \color{red}\textbf{O B S O L E T E}
  \fi
\fi
}

\lfoot{\@draftFooterText}
\rfoot{\@draftFooterText}

\cfoot{
\ifx \@controlText \@empty
  \relax
\else
\begin{minipage}{0.9\textwidth}
\centering
\vspace*{0.2cm}
\scriptsize
\bfseries
\if@isdraft
  \color{red}
  DRAFT NOT YET APPROVED
  \color{lsstfoot} --
\fi
\if@isobsolete
  \color{red}
  OBSOLETE
  \color{lsstfoot} --
\fi
\color{lsstfoot}
\@controlFootText
\if@isdraft
  --
  \color{red}
  DRAFT NOT YET APPROVED
\fi
\if@isobsolete
  --
  \color{red}
  OBSOLETE
\fi
\end{minipage}
\\
\fi
\color{black}
\thepage
}

\renewcommand{\section}{\@startsection
  {section}%                                    % the name
  {1}%                                          % the level
  {0mm}%                                        % the indent
  {-10pt \@plus -1pt \@minus -1pt}%             % the beforeskip
  {4pt \@plus 1pt}%                             % the afterskip
  {\bfseries\Large\color{lsstsect}}}%                           % the style
\renewcommand{\subsection}{\@startsection
  {subsection}%                                 % the name
  {2}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\large\color{lsstsect}}}%                      % the style
\renewcommand{\subsubsection}{\@startsection
  {subsubsection}%                              % the name
  {3}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\normalsize\color{lsstsect}}}%                      % the style


\newcommand{\gwptop}[1]{\multicolumn{1}{|l|}{\textbf{#1}}}
\newcommand{\gwpmid}[1]{\multicolumn{1}{|l|}{#1}}
\newcommand{\gwplow}[1]{\multicolumn{1}{|r|}{#1}}

% \renewcommand{\cite}{\citep}
\newcommand{\byte}{b}

%-----------------------------------------------------------------------------
%   Macros for dealing with requirements
%-----------------------------------------------------------------------------
\nplpadding{3}
\newcounter{areqi}
\renewcommand{\theareqi}{\numprint{\arabic{areqi}}}
\def\p@areq#1{\csname reqtype\endcsname-}

% default increment for requirement counter
\providecommand{\setreqincr}[1]{\setcounter{@dfreqincr}{#1}}
\newcounter{@dfreqincr}
\setcounter{@dfreqincr}{20}

\newcounter{reqincr}
\setcounter{reqincr}{\value{@dfreqincr}}

\providecommand{\newreqtype}[1]{\def\reqtype{#1}\setcounter{areqi}{0}}

\newcounter{@reqdepth}\setcounter{@reqdepth}{0}
\newenvironment{reqblock}[2][\value{@dfreqincr}]{%
\newreqtype{#2}\setcounter{reqincr}{#1}%
\addtocounter{@reqdepth}{1}}{%
\setcounter{reqincr}{\value{@dfreqincr}}%
\addtocounter{@reqdepth}{-1}}

%
%   Requirement prefix
%
\newcommand{\reqprefix}{}
\newcommand{\setReqPrefix}[1]{\renewcommand{\reqprefix}{#1}}

%
%  simplified non boxed requirement macro
%
\providecommand{\reqsimp}[1]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%

{\bf \csname p@areq\endcsname -\theareqi}  {#1}
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},"#1"}%
}

%
%  requirement macro
%
\providecommand{\req}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.11\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.22\textwidth}|% Verification
p{.11\textwidth}|% Status
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline}%
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline%
& \multicolumn{4}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%
%   B. FREZOULS 01/13/2012
%	Applicable requirement macro
%	Created from the req command with an extra argument (the last one)
% 	used to indicate to which system the req. is applicable
%	Display this argument in the requirement nomenclature
% 	and add it in the log file so that the makeReqList script can add it in the Requirements.csv file
%
\providecommand{\reqapp}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.07\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.07\textwidth}|% Verification
p{.11\textwidth}|% Status
p{.19\textwidth}|% Applicability
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6 & #7\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline}%
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline%
& \multicolumn{5}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the req command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name
%
\providecommand{\reqdel}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
%\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the reqapp command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name
%
\providecommand{\reqdel}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}


\def\defsavectr#1#2#3{%
  \expandafter\edef\csname#1#2\endcsname{#3}%
}
\newcounter{@checkreq}
\newenvironment{reqinsert}[2][\value{@dfreqincr}]{\mbox{}%
\defsavectr{@savectr}{\romannumeral\value{@reqdepth}}{\arabic{areqi}}%
\defsavectr{@saveinc}{\romannumeral\value{@reqdepth}}{\thereqincr}%
\addtocounter{@reqdepth}{1}%
\setcounter{reqincr}{#1}%
}{%
\addtocounter{@reqdepth}{-1}%
\setcounter{reqincr}{\csname @saveinc\romannumeral\the@reqdepth\endcsname}%
\setcounter{@checkreq}{\csname @savectr\romannumeral\the@reqdepth\endcsname+\value{reqincr}}%
\ifthenelse{\value{@checkreq}<\value{areqi}}{\errmessage{Requirement numbering incorrect: \the@checkreq<\arabic{areqi}}}{}%
\setcounter{areqi}{\csname @savectr\romannumeral\the@reqdepth\endcsname}}

%
%   requirement status labels
%
\providecommand{\reqiss}{Issued} % Issued requirements
\providecommand{\reqobs}{Obsolete} % Obsolete requirements
\providecommand{\reqdel}{Deleted} % Deleted requirements

% -----------------------------------------------------------------------------
% Meeting action management
% -----------------------------------------------------------------------------
\newcommand{\actprefix}{}
\newcommand{\setActionItemPrefix}[1]{\renewcommand{\actprefix}{#1}}

\newcounter{aacti}
\setcounter{aacti}{0}
\renewcommand{\theaacti}{\nplpadding{2}\numprint{\arabic{aacti}}}

\newboolean{@actstarted}
\setboolean{@actstarted}{false}
\newboolean{@oldactstarted}
\setboolean{@oldactstarted}{false}


% AI in the margin
\newcommand\marginlabel[1]{\mbox{}\marginpar{\raggedright\hspace{0pt}#1}}

% the actual action macro
% altered DWE 19/6/2008 to introduce \oldaction and \nolabelaction
%   also added hyperlinks between the actions and the action table
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\action}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\noexpand\hypertarget{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}} &
        #1 & #2 & #3\string\\\noexpand\hline}

%\vspace{-1\textheight} % does not work
\vspace{-28pt}\marginlabel{AI \hyperlink{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}}}%

\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual nolabelaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\nolabelaction}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\actprefix\arabic{aacti} & #1 & #2 & #3\string\\\noexpand\hline}
\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual oldaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\oldaction}[4]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@oldactstarted}}{\relax}{\immediate\openout8=oldactions\setboolean{@oldactstarted}{true}}
\immediate\write8{\noexpand\hypertarget{#1}{#1} & #2 & #3 & #4\string\\\noexpand\hline}
\marginlabel{AI \hyperlink{#1}{#1}}%
\typeout{AI:#1,#2,#3,#4}%
}

% Parameterized the widths of the action table in case tweaking is needed.
% DWE 3/12/08

\newcommand{\actionActionNumberWidth}{.11\textwidth}
\newcommand{\actionActioneeWidth}{.12\textwidth}
\newcommand{\actionActionDateWidth}{.12\textwidth}
\newcommand{\actionActionDescriptionWidth}{.56\textwidth}

% outputs the list of actions if any are defined
\providecommand{\listofactions}{%
\IfFileExists{actions}{%
\immediate\closeout7
\immediate\closeout8
\newcounter{actli}
\setcounter{actli}{1}
\newcommand{\countact}{\nplpadding{2}\numprint{\arabic{actli}}\addtocounter{actli}{1}}
\begin{longtable}{|p{\actionActionNumberWidth}|>{\raggedright}p{\actionActioneeWidth}|>
{\raggedright}p{\actionActionDateWidth}|p{\actionActionDescriptionWidth}|}
\hline
Id & Actionee & Due Date & Action\\\hline
\IfFileExists{oldactions}{\input{oldactions}}{}
\input{actions}
\end{longtable}
}{%
No actions have been identified.}
}

% -----------------------------------------------------------------------------
% Useful definition
% -----------------------------------------------------------------------------
\def\VRO{Vera C. Rubin Observatory~} 
\def\RO{Rubin Observatory~} 
\def\aaps{A\&AS}           % Astronomy and Astrophysics Suplement
\def\aap{A\&A}             % Astronomy and Astrophysics
\def\ssr{Space~Sci.~Rev.}  % Space Science Reviews
\def\apj{ApJ}              % Astrophysical Journal
\def\apjs{ApJS}            % Astrophysical Journal Supplement
\def\aj{AJ}                % Astronomical Journal
\def\mnras{MNRAS}          % Monthly Notices of the RAS
\def\araa{ARA\&A}          % Annual Review of Astron and Astrophys
\def\nat{Nature}           % Nature
\def\apjl{ApJ}             % Astrophysical Journal, Letters
\def\icarus{Icarus}        % Icarus
\def\prd{Phys.~Rev.~D}     % Physical Review D
\def\physrep{Phys.~Rep.}   % Physics Reports
\def\pasp{PASP}            % Publications of the Astronomical Society of the Pacific
\def\procspie{Proc.\ SPIE} % Proceedings of the SPIE
\newcommand{\pasa}{PASA}   % Publications of the Astronomical Society of Australia
\newcommand{\ao}{Appl.~Opt.}  % Applied Optics
\def\pasj{PASJ}            % Publications of the Astronomical Society of Japan

\def\degr{\hbox{$^\circ$}}
\def\arcmin{\hbox{$^\prime$}}
\def\arcsec{\hbox{$^{\prime\prime}$}}
\def\fs{\hbox{$.\!\!^{\rm s}$}}
\def\fdg{\hbox{$.\!\!^\circ$}}
\def\farcm{\hbox{$.\mkern-4mu^\prime$}}
\def\farcs{\hbox{$.\!\!^{\prime\prime}$}}
\def\sun{\hbox{$\odot$}}

%
% this makes list spacing single spaced.
%
\newenvironment{enumerate_single}{
\begin{enumerate}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{enumerate}
}
\newenvironment{itemize_single}{
\begin{itemize}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{itemize}
}

%
%   convenience macros
%
\providecommand{\pu}[2]{\ensuremath{#1\,\mbox{#2}}}
\providecommand{\secs}[1]{\pu{#1}{s}}
\providecommand{\uas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muasonly}{\ensuremath{\mu\mbox{as}}}
\providecommand{\inp}[1]{{\tt #1}}
\providecommand{\prog}[1]{{\it #1}}
\providecommand{\secref}[1]{\autoref{#1}}
\providecommand{\appref}[1]{\autoref{#1}}
\providecommand{\partref}[1]{Part~\ref{#1}}
\providecommand{\tabref}[1]{\autoref{#1}}
\providecommand{\figref}[1]{\autoref{#1}}
\providecommand{\eqnref}[1]{Eq.~\ref{#1}}
\providecommand{\reqref}[1]{Req.~\ref{#1}}
\providecommand{\actref}[1]{AI~\ref{#1}}
\providecommand{\class}[1]{{\it #1}}
\providecommand{\pack}[1]{{\em #1}}
\providecommand{\property}[1]{{\em #1}}
\providecommand{\method}[1]{{\em #1}}
\providecommand{\file}[1]{{\em #1}}
\providecommand{\directory}[1]{{\em #1}}
%\providecommand{\code}[1]{{\tt #1}}

\renewcommand{\vec}[1]{\ensuremath{\mathchoice{\mbox{\boldmath$\displaystyle#1$}}
{\mbox{\boldmath$\textstyle#1$}}
{\mbox{\boldmath$\scriptstyle#1$}}
{\mbox{\boldmath$\scriptscriptstyle#1$}}}}

%------------------ caption format ----------------------------
% added by LL to get nicer captions to tables and figures
% makecaption redefined (small, FIGURE in sc, 0.9\hsize):
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{\small {\sc #1:} #2}%
  \ifdim \wd\@tempboxa >0.9\hsize
    \hb@xt@\hsize{\hfil\parbox{0.9\hsize}{\small {\sc #1:} #2}\hfil} %\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
%------------------ end caption format ----------------------------

%----------------- Paragraph numbering - JSH

% put \npara at the start of each paragraph or \item you want to be numbered

\newcounter{@dfparincr}
\setcounter{@dfparincr}{5}

\newcounter{lsstpar}
\providecommand{\thelsstpar}{\numprint{\arabic{lsstpar}}}
\providecommand{\npara}{
\addtocounter{lsstpar}{\value{nparaincr}}
\marginlabel{\S\thelsstpar}}

% default increment for requirement counter
\providecommand{\setnparaincr}[1]{\setcounter{@dfparincr}{#1}}
\newcounter{nparaincr}
\setcounter{nparaincr}{\value{@dfparincr}}

%-----------------------


%------ REAL LSST STUFF FROM LDM-151 ----

% For referencing {description} environment labels,
% as used in DRP pipeline section.  Taken from
% http://tex.stackexchange.com/questions/1230/reference-name-of-description-list-item-in-latex
\let\orgdescriptionlabel\descriptionlabel
\renewcommand*{\descriptionlabel}[1]{%
  \let\orglabel\label
  \let\label\@gobble
  \phantomsection
  \edef\@currentlabel{#1}%
  %\edef\@currentlabelname{#1}%
  \let\label\orglabel
  \orgdescriptionlabel{#1}%
}

\newcommand{\vstretch}[1]{\vspace*{\stretch{#1}}}
\newcommand{\code}[1]{\texttt{#1}}
\newcommand{\Alert}{\code{Alert}\xspace}
\newcommand{\Alerts}{\code{Alerts}\xspace}
\newcommand{\DIASource}{\code{DIA\-Source}\xspace}
\newcommand{\DIASources}{\code{DIA\-Sources}\xspace}
\newcommand{\DIAForcedSource}{\code{DIA\-Forced\-Source}\xspace}
\newcommand{\DIAForcedSources}{\code{DIA\-Forced\-Sources}\xspace}
\newcommand{\DIAObject}{\code{DIA\-Object}\xspace}
\newcommand{\DIAObjects}{\code{DIA\-Objects}\xspace}
\newcommand{\DB}{{Level 1 database}\xspace}
\newcommand{\DR}{{Level 2 database}\xspace}
\newcommand{\PPDB}{{Prompt Products database}\xspace}
\newcommand{\DRDB}{{Data Release database}\xspace}
\newcommand{\Object}{\code{Object}\xspace}
\newcommand{\Objects}{\code{Objects}\xspace}
\newcommand{\Source}{\code{Source}\xspace}
\newcommand{\Sources}{\code{Sources}\xspace}
\newcommand{\ForcedSource}{\code{Forced\-Source}\xspace}
\newcommand{\ForcedSources}{\code{Forced\-Sources}\xspace}
\newcommand{\CoaddSource}{\code{Coadd}\xspace}
\newcommand{\Coadd}{\code{Coadd}\xspace}
\newcommand{\CoaddSources}{\code{Coadds}\xspace}
\newcommand{\Coadds}{\code{Coadds}\xspace}
% LCR-3293 removes coaddsources
\newcommand{\SSObject}{\code{SS\-Object}\xspace}
\newcommand{\SSObjects}{\code{SS\-Objects}\xspace}
\newcommand{\VOEvent}{\code{VO\-Event}\xspace}
\newcommand{\VOEvents}{\code{VO\-Events}\xspace}
\newcommand{\transSNR}{5\xspace}

% Command to link to a document in Docushare. Pass an LSST document handle as argument, or a document number.
% This will not result in a references entry.
\newcommand{\ds}[2]{{\color{blue} \href{https://docushare.lsstcorp.org/docushare/dsweb/Get/#1}{#2}}\xspace}

% Command to link to a Docushare document via a citation.

% \citeds is a "docushare citation" where the cite label used
% is the document handle rather than the year.
% citell is the Gaia version for citing livelink.
% The livelink variants are deprecated.
\newcommand{\citell}{\citeyear}
\newcommand{\citellp}{\citeyearpar}


% \citeds is preferred over \ds as it allows the document to be discovered in the references list.
% An optional argument allows the document handle to be replaced with alternate text.
% No parentheses are added around the supplied text, matching \ds, and the alternate text is blue.
% Parentheses will be added with the \citedsp variant.

% \citeds[AltText]{Handle}
\newcommand{\citeds}[2][@alttext@]{{%
\IfStrEq{#1}{@alttext@}%
{\citeyear{#2}}%
{\nocite{#2}\ds{#2}{#1}}%
}\xspace}

% Add [] around the citation text
\newcommand{\citedsp}[2][@alttext@]{{[%
\IfStrEq{#1}{@alttext@}%
{\citeds{#2}}%
{\citeds[#1]{#2}}%
}]\xspace}


\newcommand{\SRD}{\citeds[SRD]{LPM-17}}
\newcommand{\DPDD}{\citeds[DPDD]{LSE-163}}
\newcommand{\LSR}{\citeds[LSR]{LSE-29}}
\newcommand{\OSS}{\citeds[OSS]{LSE-30}}
\newcommand{\DMSR}{\citeds[DMSR]{LSE-61}}
\newcommand{\appsUMLdomain}{\citeds{LDM-133}}
\newcommand{\appsUMLusecase}{\citeds{LDM-134}}
\newcommand{\SUI}{\citeds[SUID]{LDM-131}}
\newcommand{\DMSD}{\citeds[DMSD]{LDM-148}}
\newcommand{\MOPSD}{\citeds[MOPSD]{LDM-156}}
\newcommand{\DMMD}{\citeds[DMMD]{LDM-152}}
\newcommand{\DMOps}{\citeds[DM OpsCon]{LDM-230}}
\newcommand{\SDQAP}{\citeds{LSE-63}}
\newcommand{\NewPCP}{\citeds{LSE-180}}
\newcommand{\UCAL}{\citeds[UCAL]{Document-15125}}

\newcommand{\wbsSFM}{WBS 02C.03.01}
\newcommand{\wbsAssocP}{WBS 02C.03.02}
\newcommand{\wbsAP}{WBS 02C.03.03}
\newcommand{\wbsDiffim}{WBS 02C.03.04}
\newcommand{\wbsMOPS}{WBS 02C.03.06}
\newcommand{\wbsSDQAP}{WBS 02C.01.02.02}
\newcommand{\wbsSDQAT}{WBS 02C.01.02.02}
\newcommand{\wbsSPT}{WBS 02C.01.02.03}
\newcommand{\wbsPSF}{WBS 02C.04.03}
\newcommand{\wbsCoadd}{WBS 02C.04.04}
\newcommand{\wbsDetDeblend}{WBS 02C.04.05}
\newcommand{\wbsObjChar}{WBS 02C.04.06}
\newcommand{\wbsAFW}{WBS 02C.03.05, 02C.04.01}
\newcommand{\wbsCPP}{WBS 02C.04.02}
\newcommand{\wbsPhotoCal}{WBS 02C.03.07}
\newcommand{\wbsAstroCal}{WBS 02C.03.08}



%%% Command's for merging Robert's document, at least temporarily.
%%% Some of these will be removable, some may not be.
\renewcommand{\c}{\textit{c.}\xspace}
\newcommand{\eg}{\textit{e.g.}\xspace}
\newcommand{\etc}{\textit{etc.}\xspace}
\newcommand{\ie}{\textit{i.e.}\xspace}
\renewcommand{\th}{\ensuremath{^{\mbox{\tiny th}}}\xspace}
\newcommand{\Nb}{\textit{N.b.}\xspace}
\newcommand{\nb}{\textit{n.b.}\xspace}
\DeclareBoldMathCommand\xib{\xi}
\DeclareBoldMathCommand\zerob{0}
\newcommand{\cameraTeam}{\textbf{Camera Team deliverable}\\}
\newcommand{\TBD}{\textit{T.B.D.}\xspace}
\if@isdraft
\newcommand{\XXX}[1]{{{\color{red}\textbf{XXX #1}\xspace}}}
\else
\newcommand{\XXX}[1]{}
\fi
\newcommand{\myLabel}[2]{\def\@currentlabel{#2}\label{#1}}
\newcommand{\appRef}[1]{App. \ref{app:#1}}
\newcommand{\secRef}[1]{Sec. \ref{sec:#1}}
\newcommand{\rednote}[1]{{\color{red} (#1)}}

\newcommand{\alg}{\\ \textbullet\xspace Algorithmic component: }
\newcommand{\fefiftyfive}{$^{55}$Fe\xspace}
\newcommand{\bfeffect}{``brighter-fatter effect"}
\newcommand{\auxtelescope}{auxiliary/Calpyso/calibration telescope\xspace}
\newcommand{\secsymbol}{§}
\newcommand{\xxx}{{\color{red} xxx}\xspace}
\newcommand{\dragons}{ {\color{blue} \textbf{\textit{Here be dragons...}}}}
\newcommand{\mysubitem}{\subitem \textendash\xspace}
\newcommand{\smalltilde}{\raise.26ex\hbox{$\scriptstyle\mathtt{\sim}$}}
\newcommand{\electron}{$e^{-}$}

%%%%% Commands for indicating added text and removed text
\newcommand{\oldtext}[1]{{\color{red} #1}}
\newcommand{\newtext}[1]{{\color{blue} #1}}

%%%%% Commands for adding requirement numbers to margins
\newcommand{\margin@req}[1]{\marginpar{\hspace{0pt}\tiny #1}}

% DMSR, LSR and OSS requirements have their own command
\newcommand{\dmreq}[1]{\margin@req{DMS-REQ-#1}}
\newcommand{\lsrreq}[1]{\margin@req{LSR-REQ-#1}}
\newcommand{\ossreq}[1]{\margin@req{OSS-REQ-#1}}

% Used for requirements parameters/constraints
\newcommand{\reqparam}[1]{\margin@req{#1}}

% Reference a JIRA ticket
\newcommand{\jira}[1]{\href{https://jira.lsstcorp.org/browse/#1}{#1}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% We have multiple types of note environments.
%% They all have titles that can be over ridden and are in colored boxes.
%% "note" is the basic type. Title will default to Note but will not force that prefix.
%% "warning" has a Warning prefix and different color
%% "draftnote" is special in that the comment will not be shown unless the document is draft mode (lsstdraft).

%% Generic note that takes four arguments: background color, frame color, prefix text, title text
\newenvironment{admonition}[4]
{
  \@ifmtarg{#3}%
  {% Empty prefix
    \@ifmtarg{#4}{\def\@ttext{Admonition}}{\def\@ttext{#4}}
  }{% Prefix
    \@ifmtarg{#4}{\def\@ttext{#3}}{\def\@ttext{#3: #4}}
  }

  \begin{minipage}[h]{.75\linewidth}
    \begin{tcolorbox}[colback=#1,colframe=#2,title=\@ttext]
}
{
    \end{tcolorbox}
  \end{minipage}
}

\newenvironment{warning}[1][]
{
  \begin{admonition}{orange!5!white}{orange!75!black}{Warning}{#1}
}
{
  \end{admonition}
}

\newenvironment{note}[1][Note]
{
  \begin{admonition}{cyan!5!white}{cyan!75!black}{}{#1}
}
{
  \end{admonition}
}

\if@isdraft
  \newenvironment{draftnote}[1][]
  {
    \begin{admonition}{green!5!white}{green!75!black}{Comment for draft}{#1}
  }
  {
    \end{admonition}
  }
\else
  % Empty environment that is excluded
  \newenvironment{draftnote}[1][]
  {}
  {}
  \excludecomment{draftnote}
\fi

\newcommand{\uc}[1]{\texttt{#1}}
