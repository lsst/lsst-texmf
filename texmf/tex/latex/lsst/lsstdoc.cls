%%------------------------------------------------------------
%% General LSST  document class --- copied from Gaia by wil
%%------------------------------------------------------------
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{lsstdoc}[2016/12/12 v1.1 LSST document class]

\LoadClass[11pt,letterpaper]{article}

% Define the default stretch
\renewcommand{\baselinestretch}{1.25}

% LSST uses a sans serif font
\RequirePackage{ifxetex}
\ifxetex
  \RequirePackage{fontspec}
  \RequirePackage{xunicode}
  \defaultfontfeatures[OpenSans]
  {
  Extension = .ttf ,
  UprightFont = OpenSans-Regular,
  BoldFont = OpenSans-Bold,
  ItalicFont = OpenSans-Italic,
  BoldItalicFont = OpenSans-BoldItalic
  }
  \setmainfont[Ligatures=TeX]{OpenSans}
  \setmonofont{Inconsolata}
\else
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8x]{inputenc}
  \RequirePackage[default]{opensans}
  \RequirePackage{inconsolata}
\fi

\RequirePackage[usenames]{xcolor}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsbsy}
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

%\RequirePackage[linkcolor=blue,colorlinks=true]{hyperref}
\RequirePackage{hyperref}
\RequirePackage{numprint}
\RequirePackage[english,iso]{isodate}
\RequirePackage{titlesec}
\RequirePackage[english]{babel}
\RequirePackage{tabularx}
%\RequirePackage{comment}
\RequirePackage{xspace}
\RequirePackage{xstring}
%\RequirePackage{microtype}
\RequirePackage{listings}
%\RequirePackage{nameref}
%\RequirePackage{mathptmx} % note this messes up \vec definition... do not e add put in your doc if you want it

% Standardize bibliography styling
\bibliographystyle{lsst_aa}

% The standard word template uses different blue for
% title, section headings and the banner.
% define lsstblue as the banner color
\definecolor{lsstblue}{RGB}{ 69,106,153}
\definecolor{lsstsect}{RGB}{ 23, 54, 93}
\definecolor{lssttitle}{RGB}{ 54, 95,145}
\definecolor{lssthead}{RGB}{ 79,129,189}

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
% Define the CUs -- and the DPACE
%
\DeclareOption{DM}{
   \renewcommand{\CU}{DM}
   \renewcommand{\docType}{Data Management}
}
\DeclareOption{SE}{
   \renewcommand{\CU}{SE}
   \renewcommand{\docType}{Systems Engineering}
}

%
% default settings for the newly defined commands
%

% you own DPC, institute or funding logo for front page
\newcommand{\setDocLocalLogo}[1]{\def\@docLocalLogo{#1}}
\setDocLocalLogo{}

\newcommand{\docType}{LSST Document}
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

\newcommand{\docTitle}{No Title}
\providecommand{\setDocTitle}[2][@shorttitle@]{
  \def\@docTitle{\Huge #2}
  \ifthenelse{\equal{@shorttitle@}{#1}}
             {\def\@docShortTitle{}}
             {\def\@docShortTitle{#1}}
  \renewcommand{\docTitle}{#2}
}

\newcommand{\docSubtitle}{No Subtitle}
\newcommand{\setDocSubtitle}[1]{\def\@docSubtitle{#1}
  \renewcommand{\docSubtitle}{#1}
}
\setDocSubtitle{}

\newcommand{\setDocCompact}[1]{\def\@docCompact{#1}}
\setDocCompact{}
\def\@docCompact{false}

\setDocTitle{Set the document title with $\backslash$setDocTitle}

\newcommand{\docDate}{set the date with {$\backslash$}setDocDate}
\newcommand{\setDocDate}[1]{\renewcommand{\docDate}{#1}}

% allow standard \date{} to work as an alias of \setDocDate
\renewcommand{\date}[1]{\setDocDate{#1}}

\newcommand{\docIssue}{none}
\newcommand{\setDocIssue}[1]{\renewcommand{\docIssue}{#1}}

\newcommand{\docStatus}{set the Status with {$\backslash$}setDocStatus}
\newcommand{\setDocStatus}[1]{\renewcommand{\docStatus}{#1}}

\newcommand{\docRevision}{set the Revision with {$\backslash$}setDocRevision}
\newcommand{\setDocRevision}[1]{\renewcommand{\docRevision}{#1}}

\newif\if@dmtct
\@dmtctfalse
\newif\if@ccb
\@ccbfalse
\newcommand{\docRef}{set the Reference with {$\backslash$}setDocRef}
\newcommand{\setDocRef}[1]{
   \renewcommand{\docRef}{#1}
   \if@dmtct\relax\else\IfBeginWith{#1}{LDM-}{\@dmtcttrue}{}\fi
   \if@ccb\relax\else\IfBeginWith{#1}{LSE-}{\@ccbtrue}{}\fi
}

\newcommand{\docAuthor}{set the Author with {$\backslash$}setDocAuthor}
\newcommand{\setDocAuthor}[1]{\renewcommand{\docAuthor}{#1}}

\newcommand{\setDocCurator}[1]{\def\@docCurator{#1}}
\setDocCurator{}

\newcommand{\setDocAffil}[1]{\def\@docAffil{#1}}
\setDocAffil{}

\newcommand{\docApprove}{@noapprove@}
\newcommand{\setDocApprove}[1]{\renewcommand{\docApprove}{#1}}

\newcommand{\docAuthorize}{@noauthorize@}
\newcommand{\setDocAuthorize}[1]{\renewcommand{\docAuthorize}{#1}}

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

\providecommand{\putlogo}{
  \begin{center}
	\includegraphics{lsst_logo_notext}\\
   \end{center}
\vspace{-25pt}
\color{lsstblue}
   \hspace{-2.8cm}\rule{6.15cm}{2.5pt} \lower.3em\hbox{
	{\Large \color{lsstblue}LARGE SYNOPTIC SURVEY TELESCOPE}
   }
   \rule{7.0cm}{2.5pt}

  \begin{center}
    \ifx \@docLocalLogo \@empty
           \relax
     \else
           \includegraphics{\@docLocalLogo}
    \fi
   \end{center}
}



\newcommand{\mkshorttitle}{
     \begin{center}
        \@docTitle \\
        \normalsize {\bf \docAuthor}\\
	Issue \docIssue.\docRevision ~~ \docDate\\
     \end{center}

}

\renewcommand{\maketitle}{
  \hypersetup{pdftitle={\@title\ifx\@docSubtitle\@empty\else\ - \docSubtitle\fi},
  pdfauthor={\@author},
  pdfkeywords={\docRef}}

   \thispagestyle{empty}

    \AddToShipoutPicture*{%
            \setlength{\unitlength}{0.7pt}%
        \makeatletter
            \put(\strip@pt \textwidth,\strip@pt \textheight){%
                \makebox(0,0){%
			\includegraphics[scale=0.9]{lsstscopegrey}\\
                    }}%
		\vspace{10cm}
		{\hspace{-0.5in}\color{lsstblue}\rule{9in}{2.1cm}}

        \makeatother
    }%

   \setlength{\parindent}{0pt}
   \vspace*{-5cm}
   \putlogo
   \vspace*{1cm}
   \begin{center}
   \begin{minipage}{1.0\textwidth}
     \begin{center}
    \color{lssttitle}
    \textsf{\LARGE \bfseries Large Synoptic Survey Telescope (LSST)} \\
    \vspace*{0.5cm}
    \textsf{\Huge \bfseries \@title} \\
      \ifx \@docSubtitle \@empty
       \relax
    \else
         \vspace*{1cm}
         \large\@docSubtitle
    \fi
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

   % Define the control text to use based on document type
   \def\@controlText{}
   \def\@controlFootText{}
   \if@ccb
   \def\@controlText{%
   This LSST document has been approved as a Content-Controlled Document.
   Its contents are subject to configuration control and may not be changed, altered, or their provisions waived without prior approval.
   If this document is changed or superseded, the new document will retain the Handle designation shown above.
   The control is on the most recent digital document with this Handle in the LSST digital archive and not printed versions.
   }
   \def\@controlFootText{%
   The contents of this document are subject to configuration control and may not be changed, altered, or their provisions waived without prior approval.
   }
   \fi
   \if@dmtct
   \def\@controlText{%
   This LSST document has been approved as a Content-Controlled Document by the LSST DM Technical Control Team.
   If this document is changed or superseded, the new document will retain the Handle designation shown above.
   The control is on the most recent digital document with this Handle in the LSST digital archive and not printed versions.
   Additional information may be found in the corresponding DM RFC.
   }
   \def\@controlFootText{%
   The contents of this document are subject to configuration control by the LSST DM Technical Control Team.
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
   \else
     \begin{spacing}{1.5}
       \textbf{\small
       \if@isdraft
         \color{red}
         Draft Revision NOT YET Approved
         \color{black} --
       \fi
       \color{black}
       \@controlText
       \if@isdraft
       -- \color{red} Draft Revision NOT YET Approved
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
   {\large\textsf{
      \begin{tabbing}
         XXXXXXXXX: \=\kill
    \ifx \@docAffil \@empty
     \relax
     \else
         affiliation :\> \@docAffil\\
    \fi
    \ifx \@docCurator \@empty
         \relax
         \else
         curator:\> \@docCurator\\
     \fi
    \ifthenelse{\equal{@noapprove@}{\docApprove}}%
    {}{approved by:\> \docApprove\\}%
    \ifthenelse{\equal{@noauthorize@}{\docAuthorize}}%
    {}{authorized by:\> \docAuthorize\\}%
\ifthenelse{\equal{\docIssue}{none}}{\relax}{%
         issue:\>       \docIssue\\}%
revision:\>    \docRevision\\
         status:\>      \docStatus
      \end{tabbing}
   }}

    \ifx \@docCompact \@empty
           \pagebreak
     \else
     \relax
    \fi
   \pagenumbering{roman}
   \docAbstract
   \docChangeRecord

   \if@addtoc
     \setcounter{tocdepth}{3}
     % Do not use lots of whitespace in toc
     \begin{spacing}{0.8}
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
%   \addtocounter{table}{-1}
    \begin{longtable}{|l|p{.15\textwidth}|p{.45\textwidth}|p{.23\textwidth}|}

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
\setlength{\textwidth}{6.5in}
\setlength{\textheight}{8.5in}

\setlength{\topmargin}{0cm}
\setlength{\oddsidemargin}{0cm}
\setlength{\evensidemargin}{0cm}
\setlength{\leftmargin}{1in}
\setlength{\marginparwidth}{1in}

\setlength{\parindent}{0cm}             % No indent at start of paragraphs
\setlength{\parskip}{\baselineskip}     % Blank line between paragraph

\setlength\headheight{15pt}     % Make space for logo

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
\setcounter{tocdepth}{4}       % appearance level in table of contents

\pagestyle{fancy}

\addtolength{\headsep}{4.2mm}

% Shift everything up a bit
\setlength{\topmargin}{-0.5cm}

\fancyheadoffset{0pt}
\lhead{
\color{lsstblue}
 \vspace{-4cm}
  \IfFileExists{lsst_logo_notext.png}{
    \resizebox{0.18\textwidth}{!}{\includegraphics{lsst_logo_notext}}
    %\hspace{5pt}{\bfseries\large\sf{\CU\DU}}
  } {
       {\bfseries\large\sf{LSST: \CU\DU}}
  }\\\vspace{-8pt}
\color{lsstblue}
\begin{minipage}{7.5in}
%    \hspace{-1.5cm}\rule{0.55cm}{1.0pt} \lower.1em\hbox{
    \hspace{-1.8cm}\rule{1.4cm}{2.0pt} \lower.1em\hbox{
	{ \hspace{-0.1cm}\tiny \color{lssthead}LARGE SYNOPTIC SURVEY TELESCOPE}\hspace{-0.1cm}
   }
    \color{lsstblue}
    \rule{14.8cm}{2.0pt}
\end{minipage}
\vspace{-30pt}
\begin{flushright}
\begin{minipage}{12.5cm}
\tiny
\sffamily
\begin{tabularx}{\textwidth}{XXr}
\@docShortTitle & \docRef~ \docStatus & Latest Revision \docDate \\
\end{tabularx}
\end{minipage}
\end{flushright}
  \vskip -2\baselineskip
}

\rhead{
}

\renewcommand{\headrulewidth}{0.0pt}

\renewcommand{\footrulewidth}{1pt}

% If this is not a controlled document we have space for DRAFT in the left and right footer
\newcommand{\@draftFooterText}{
\ifx \@controlText \@empty
  \if@isdraft
    \color{red}\textbf{D R A F T}
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
\begin{center}
  \vspace*{0.2cm}
  \scriptsize
  \bfseries
  \if@isdraft
    \color{red}
    DRAFT NOT YET APPROVED
    \color{lssthead} --
  \fi
  \color{lssthead}
  \@controlFootText
  \if@isdraft
    --
    \color{red}
    DRAFT NOT YET APPROVED
  \fi
\end{center}
\end{minipage}
\fi
\vspace*{-0.25cm}
\begin{center}
\color{black}
\thepage
\end{center}
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

\makeatother

% \renewcommand{\cite}{\citep}
\newcommand{\byte}{b}

%-----------------------------------------------------------------------------
%   Macros for dealing with requirements
%-----------------------------------------------------------------------------
\makeatletter
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
\makeatother

%
%   requirement status labels
%
\providecommand{\reqiss}{Issued} % Issued requirements
\providecommand{\reqobs}{Obsolete} % Obsolete requirements
\providecommand{\reqdel}{Deleted} % Deleted requirements

% -----------------------------------------------------------------------------
% Meeting action management
% -----------------------------------------------------------------------------
\makeatletter
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
\providecommand{\secref}[1]{Section~\ref{#1}}
\providecommand{\appref}[1]{Appendix~\ref{#1}}
\providecommand{\partref}[1]{Part~\ref{#1}}
\providecommand{\tabref}[1]{Table~\ref{#1}}
\providecommand{\figref}[1]{Figure~\ref{#1}}
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

\newcounter{gaiapar}
\providecommand{\thegaiapar}{\numprint{\arabic{gaiapar}}}
\providecommand{\npara}{
\addtocounter{gaiapar}{\value{nparaincr}}
\marginlabel{\S\thegaiapar}}

% default increment for requirement counter
\providecommand{\setnparaincr}[1]{\setcounter{@dfparincr}{#1}}
\newcounter{nparaincr}
\setcounter{nparaincr}{\value{@dfparincr}}

%-----------------------


%------ REAL LSST STUFF FROM LDM-151 ----

% For referencing {description} environment labels,
% as used in DRP pipeline section.  Taken from
% http://tex.stackexchange.com/questions/1230/reference-name-of-description-list-item-in-latex
\makeatletter
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
\makeatother


\newcommand{\vstretch}[1]{\vspace*{\stretch{#1}}}
\newcommand{\code}[1]{\texttt{#1}}

\newcommand{\Alert}{\code{Alert}\xspace}
\newcommand{\Alerts}{\code{Alerts}\xspace}
\newcommand{\DIASource}{\code{DIASource}\xspace}
\newcommand{\DIASources}{\code{DIASources}\xspace}
\newcommand{\DIAObject}{\code{DIAObject}\xspace}
\newcommand{\DIAObjects}{\code{DIAObjects}\xspace}
\newcommand{\DB}{{Level 1 database}\xspace}
\newcommand{\DR}{{Level 2 database}\xspace}
\newcommand{\Object}{\code{Object}\xspace}
\newcommand{\Objects}{\code{Objects}\xspace}
\newcommand{\Source}{\code{Source}\xspace}
\newcommand{\Sources}{\code{Sources}\xspace}
\newcommand{\ForcedSource}{\code{ForcedSource}\xspace}
\newcommand{\ForcedSources}{\code{ForcedSources}\xspace}
\newcommand{\CoaddSource}{\code{CoaddSource}\xspace}
\newcommand{\CoaddSources}{\code{CoaddSources}\xspace}
\newcommand{\SSObject}{\code{SSObject}\xspace}
\newcommand{\SSObjects}{\code{SSObjects}\xspace}
\newcommand{\VOEvent}{\code{VOEvent}\xspace}
\newcommand{\VOEvents}{\code{VOEvents}\xspace}
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
\newcommand{\xib}{{\boldsymbol \xi}}
\newcommand{\zerob}{{\boldsymbol 0}}
\newcommand{\cameraTeam}{\textbf{Camera Team deliverable}\\}
\newcommand{\TBD}{\textit{T.B.D.}\xspace}
\newcommand{\XXX}[1]{{{\color{red}\textbf{XXX #1}\xspace}}}
\makeatletter
\newcommand{\myLabel}[2]{\def\@currentlabel{#2}\label{#1}}
\makeatother
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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



\newenvironment{note}[1][Note]
{
  \begin{displaymath}
    \left[ \qquad
    \begin{minipage}[h]{.75\linewidth}
      \color{red} \footnotesize
      \textbf{#1:} \newline
      \color{black}
}
{
    \end{minipage}
    \normalsize
    \qquad \right]
  \end{displaymath}
}

\newcommand{\uc}[1]{{\tt #1}}
