% filename: csm.cls
\NeedsTeXFormat{LaTeX2e}
\def\fileversion{1.0}
\def\filedate{2013/10/01}
\ProvidesClass{csm}[\filedate \space v\fileversion \space (scmde)]
\ProvidesFile{csm.cls}[\filedate \space v\fileversion \space (scmde)]
\typeout{------------------------------}
\typeout{          csm.cls             }
\typeout{------------------------------}

% options
\newif\if@exercise\@exercisetrue
\newif\if@handout\@handoutfalse
\newif\if@lecture\@lecturefalse
\newif\if@exampaper\@exampaperfalse
\newif\if@cymraeg\@cymraegfalse
\newif\if@solutions\@solutionsfalse
\newif\if@blanks\@blanksfalse

% command line option
\ifnum\interactionmode = 2
	\def\optionYes{Y}
	\def\optionNo{N}
	\ifx\cymraeg\undefined\typein[\cymraeg]{Cymraeg? (Y/N)}\fi
	\ifx\cymraeg\optionYes\@cymraegtrue\fi
	\ifx\solutions\undefined\typein[\solutions]{Solutions? (Y/N)}\fi
	\ifx\solutions\optionYes\@solutionstrue\fi
	\ifx\blanks\undefined\typein[\blanks]{Blanks? (Y/N)}\fi
	\ifx\blanks\optionYes\@blankstrue\fi
\fi

% class options
\DeclareOption{exercise}{\@exercisetrue}
\DeclareOption{handout}{\@handouttrue\@exercisefalse}
\DeclareOption{lecture}{\@lecturetrue\@exercisefalse}
\DeclareOption{exampaper}{\@exampapertrue\@exercisefalse}
\DeclareOption{cym}{\ifx\cymraeg\undefined\@cymraegtrue\else\message{^^J'cym' option has no effect^^J}\fi}
\DeclareOption{solutions}{\ifx\solutions\undefined\@solutionstrue\else\message{^^J'solutions' option has no effect^^J}\fi}
\DeclareOption{blanks}{\ifx\blanks\undefined\@blankstrue\else\message{^^J'blanks' option has no effect^^J}\fi}
\ProcessOptions
\relax

% message
\message{>>>>> OPTIONS:}
\if@cymraeg\message{ CYMRAEG}\fi
\if@solutions\message{ SOLUTIONS}\fi
\if@blanks\message{ BLANKS}\fi
\message{<<<<<}

% load class
\if@exampaper
	\LoadClass[12pt]{exam}
\else
	\LoadClass{exam}
\fi


% set exam class booleans
\if@solutions
	\printanswers
\else
	\renewcommand{\printanswers}{}
\fi

% import common packages
\RequirePackage{amsmath,amsfonts}
\RequirePackage{xcolor}
\RequirePackage{geometry}

% default fonts
\renewcommand{\rmdefault}{ptm}
\renewcommand{\sfdefault}{phv}
\renewcommand{\ttdefault}{pcr}
\renewcommand{\familydefault}{\rmdefault}

\renewcommand{\labelenumi}{(\alph{enumi})}
\renewcommand{\labelenumii}{(\roman{enumii})}

% today in GB date format
%\def\today{\number\day\space\ifcase\month\or January \or February \or March \or April \or May \or June \or July \or August \or September \or October \or November \or December \fi \number\year}
%\def\today{\number\day\space\ifcase\month\or Jan \or Feb \or Mar \or Apr\or May \or Jun \or Jul \or Aug \or Sep \or Oct \or Nov \or Dec \fi \number\year}
\def\today{\number\day/\number\month/\number\year}

%------------------------------------------------------------------------------
% meta information
%------------------------------------------------------------------------------
\newcommand{\modulecode}[1]{\newcommand{\themodulecode}{#1}}
\newcommand{\moduletitle}[1]{\newcommand{\themoduletitle}{#1}}
\newcommand{\academicyear}[1]{\newcommand{\theacademicyear}{#1}}
\newcommand{\doctype}[1]{\newcommand{\thedoctype}{#1}}
\newcommand{\docversion}[1]{\newcommand{\thedocversion}{#1}}

\newcommand{\thedoctitle}{}
%\newcommand{\doctitle}[1]{\newcommand{\thedoctitle}{#1}}
\newcommand{\thedocnumber}{}
%\newcommand{\docnumber}[1]{\renewcommand{\thedocnumber}{#1}}

\newcommand{\doctitle}[1]{\ifdefined\thedoctitle\renewcommand{\thedoctitle}{#1}\else\newcommand{\thedoctitle}{#1}\fi}
\newcommand{\docnumber}[1]{\ifdefined\thedocnumber\renewcommand{\thedocnumber}{#1}\else\newcommand{\thedocnumber}{#1}\fi}


%\newcommand{\lecturetitle}[1]{\renewcommand{\thedoctitle}{#1}}
%\newcommand{\lecturenumber}[1]{\renewcommand{\thedocnumber}{#1}}
\newcommand{\lecturetitle}[1]{\ifdefined\thelecturetitle\renewcommand{\thelecturetitle}{#1}\else\newcommand{\thelecturetitle}{#1}\fi}
\newcommand{\lecturenumber}[1]{\ifdefined\thelecturenumber\renewcommand{\thelecturenumber}{#1}\else\newcommand{\thelecturenumber}{#1}\fi}


% meta names
\newcommand{\academicyearname}{Year}
\newcommand{\modulename}{Module}
\newcommand{\modulecodename}{Code}
\newcommand{\moduletitlename}{}
\newcommand{\doctypename}{}	
\newcommand{\doctitlename}{Subject}
\newcommand{\docnumbername}{Number}
\newcommand{\handoutdatename}{Hand-out date}
\newcommand{\handindatename}{Hand-in date}	
\newcommand{\creditname}{Credit}
\newcommand{\versionname}{Version}
\newcommand{\instructionsname}{Instructions}
\if@cymraeg
	\renewcommand{\academicyearname}{Cyfnod}
	\renewcommand{\modulename}{Modiwl}
	\renewcommand{\modulecodename}{Cod}
	\renewcommand{\moduletitlename}{}
	\renewcommand{\doctypename}{}
	\renewcommand{\doctitlename}{Pwnc}
	\renewcommand{\docnumbername}{Rhif}
	\renewcommand{\handoutdatename}{Gosodwyd}
	\renewcommand{\handindatename}{Cyflwynir}	
	\renewcommand{\creditname}{Marciau}
	\renewcommand{\versionname}{Fersiwn}
	\renewcommand{\instructionsname}{Cyfarwyddiadau}
\fi	
\if@cymraeg
	\renewcommand{\solutiontitle}{\noindent\textbf{Ateb: }}
\fi


% defaults
%\@ifundefined{thedocversion}{Version: \today}{Version: \thedocversion}

%------------------------------------------------------------------------------
% common
%------------------------------------------------------------------------------

\newenvironment{steps}{\begin{enumerate}}{\end{enumerate}}
\newcommand{\step}[1]{\item {{#1}}}


%------------------------------------------------------------------------------
% option: handout
%------------------------------------------------------------------------------
\if@handout
	\typeout{------------------------------}
	\typeout{ csm:handout				   }
	\typeout{------------------------------}

	% page layout
	\geometry{left=20mm,right=30mm,top=30mm,bottom=30mm,a4paper}
	
	% tweaks
	\renewcommand{\questionshook}{\addtolength{\itemsep}{3ex}}
	\renewcommand{\subpartlabel}{(\thesubpart)}


	% headers and footers
	\runningheadrule
	\lhead[]{\textsl{\thedoctype}}
	\chead[]{\textsl{\themodulecode}}
	\rhead[]{\textsl{\theacademicyear}}
	\lfoot[]{{\ttfamily\tiny\versionname:\ \today}}
	\rfoot{\thepage}
	\cfoot{}

	% theorems
	\RequirePackage{amsmath,amsfonts,amssymb}
	\RequirePackage[hyperref, thmmarks, amsmath]{ntheorem}
	\theoremstyle{break}
	\setlength\theorempreskipamount{3ex}
	\setlength\theorempostskipamount{2ex}
	\theorembodyfont{\upshape}
%	\newcommand{\qed}{\mbox{}\hfill$\Box$}
	\qedsymbol{\rule{1ex}{1ex}}

	\newtheorem{theorem}{Theorem}
	\newtheorem{hypothesis}[theorem]{Hypothesis}
	\newtheorem{definition}[theorem]{Definition}
	\newtheorem{lemma}[theorem]{Lemma}
	\newtheorem{proposition}[theorem]{Proposition}
	\newtheorem{corollary}[theorem]{Corollary}
	\newtheorem{remark}[theorem]{Remark}
	\newtheorem{example}[theorem]{Example}
	\newtheorem{exercise}[theorem]{Exercise}
	\newenvironment{examplecont}[1]{\textbf{Example~{#1}} (\textsl{continued})\par}{\vspace*{2ex}}
	
%	% maketitle and watermark 
	\AtBeginDocument{
	\maketitle
	}
	
	% make title 
	\renewcommand{\maketitle}{%
		\hrule\vspace{0.25ex}\hrule\vspace{1ex}
		\noindent
		\ttfamily
		\begin{tabular}{l}
		\@ifundefined{themodulecode}{}{\themodulecode\ \@ifundefined{themoduletitle}{}{\themoduletitle}\ \@ifundefined{theacademicyear}{}{\theacademicyear} \\}
		\@ifundefined{thedoctype}{}{\thedoctype\ \@ifundefined{thedocnumber}{}{\thedocnumber} \\[1ex]}
		\@ifundefined{thedoctitle}{}{\thedoctitle \\}
		\end{tabular}
		\normalsize\normalfont
		\vspace{0.5ex}\hrule\vspace{0.25ex}\hrule\vspace{3ex}
	}
\fi 

%------------------------------------------------------------------------------
% option: exercise
%------------------------------------------------------------------------------
\if@exercise
	\typeout{------------------------------}
	\typeout{ csm:exercise				  }
	\typeout{------------------------------}

	% meta
	\newcommand{\handindate}[1]{\newcommand{\thehandindate}{#1}}
	\newcommand{\handoutdate}[1]{\newcommand{\thehandoutdate}{#1}}
	\newcommand{\credit}[1]{\newcommand{\thecredit}{#1}}

	% class options
	\bracketedpoints
	\pointsinrightmargin
	\pointsdroppedatright
	\addpoints
	
	% page layout
	\geometry{left=20mm,right=30mm,top=30mm,bottom=30mm,a4paper}
	
	% tweaks
	\renewcommand{\questionshook}{\addtolength{\itemsep}{3ex}}
	\renewcommand{\subpartlabel}{(\thesubpart)}

	% instructions environment
	\RequirePackage{verbatim}
	\newenvironment{instructions}{}{}
	\ifprintanswers
		\renewenvironment{instructions}{\comment}{\endcomment}
	\else
		\renewenvironment{instructions}{%
			\vspace*{1ex}\hrule\vspace*{1ex}
			\begin{minipage}{0.9\linewidth}
			\mbox{}\par
			\textbf{\underline{\instructionsname}}\par
		}{%
			\end{minipage}
			\vspace*{2.5ex}\hrule\vspace*{2ex}
		}
	\fi

	% headers and footers
	\runningheadrule
	\lhead[]{\textsl{\thedoctype}}
	\chead[]{\textsl{\themodulecode}}
	\rhead[]{\textsl{\theacademicyear}}
	\lfoot[]{{\ttfamily\tiny\versionname:\ \today}}
	\rfoot{\thepage}
	\cfoot{}
	
%	% maketitle and watermark 
	\AtBeginDocument{
	\maketitle
	\ifprintanswers
		\usepackage{draftwatermark}
		\SetWatermarkLightness{0.95}
		\if@cymraeg
			\SetWatermarkText{ATEBION}
		\else
			\SetWatermarkText{SOLUTIONS}
		\fi
		\SetWatermarkAngle{60}
	\fi
	}
	
	% make title 
	\renewcommand{\maketitle}{%
		\hrule\vspace{0.25ex}\hrule\vspace{1ex}
		\noindent
		\ttfamily
		\begin{tabular}{l}
		\@ifundefined{themodulecode}{}{\themodulecode\ \@ifundefined{themoduletitle}{}{\themoduletitle}\ \@ifundefined{theacademicyear}{}{\theacademicyear} \\}
		\@ifundefined{thedoctype}{}{\thedoctype\ \@ifundefined{thedocnumber}{}{\thedocnumber} \\[1ex]}
		\@ifundefined{thedoctitle}{}{\thedoctitle \\}
		\@ifundefined{thehandoutdate}{}{\handoutdatename:\ \thehandoutdate \\}
		\@ifundefined{thehandindate}{}{\handindatename:\ \thehandindate \\}
		\@ifundefined{thecredit}{}{\creditname\ \thecredit \\}
		\end{tabular}
%		\begin{tabular}{ll}
%		\@ifundefined{theacademicyear}{}{\academicyearname	& \theacademicyear \\}
%		\@ifundefined{themodulecode}{}{\modulename			& \themodulecode
%			\@ifundefined{themoduletitle}{}{ \themoduletitle}	\\}
%		\@ifundefined{thedoctype}{}{\doctypename			& \thedoctype \\}
%		\@ifundefined{thedoctitle}{}{\doctitlename		& \thedoctitle \\}
%		\@ifundefined{thedocnumber}{}{\docnumbername			& \thedocnumber \\}
%		\@ifundefined{thehandoutdate}{}{\handoutdatename		& \thehandoutdate \\}
%		\@ifundefined{thehandindate}{}{\handindatename			& \thehandindate \\}
%		\@ifundefined{thecredit}{}{\creditname				& \thecredit \\}
%		\end{tabular}
		\normalsize\normalfont
		\vspace{0.5ex}\hrule\vspace{0.25ex}\hrule\vspace{3ex}
	}
\fi 

%------------------------------------------------------------------------------
% lecture option
%------------------------------------------------------------------------------
\if@lecture
	\typeout{------------------------------}
	\typeout{ csm: lecture				  }
	\typeout{------------------------------}

	% fonts
	\renewcommand{\familydefault}{\sfdefault}
	\usepackage[T1]{fontenc}
	\usepackage{lmodern}
	\usepackage{exscale} 
	\usepackage{scrextend}
	\changefontsizes{20pt}

	% layout (A4 landscape)
	\geometry{paperwidth=297mm, paperheight=210mm	}
	\geometry{left=15mm,right=15mm,top=18mm,bottom=18mm}
	
	% numbering
	\renewcommand{\questionshook}{\addtolength{\itemsep}{3ex}}
	\renewcommand{\subpartlabel}{(\thesubpart)}
	
	% spacing
	\setlength{\parindent}{0ex}
	\addtolength{\topskip}{4ex}
	\addtolength{\tabcolsep}{1ex}
	\renewcommand{\arraystretch}{1.3}
	\addtolength{\arraycolsep}{0.5ex}

	% custom itemize (slides)
	\renewenvironment{itemize}{%
	\begin{list}{$\bullet$\ }{%
	    \setlength{\itemsep}{0ex plus 0.2ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	    \setlength{\topsep}{1ex}
	}}{\end{list}}
	
	% re-define enumerate environment
	\renewenvironment{enumerate}{%
	\begin{list}{(\arabic{enumi})}{%
	    \usecounter{enumi}
	    \setlength{\itemsep}{0.25ex plus 0.15ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	}} {\end{list}}


	% theorems
	\RequirePackage{amsmath,amsfonts,amssymb}
	\RequirePackage[hyperref, thmmarks, amsmath]{ntheorem}
	\theoremstyle{break}
	\setlength\theorempreskipamount{3ex}
	\setlength\theorempostskipamount{2ex}
	\theorembodyfont{\upshape}
%	\newcommand{\qed}{\mbox{}\hfill$\Box$}
	\qedsymbol{\rule{1ex}{1ex}}

	\newtheorem{theorem}{Theorem}
	\newtheorem{hypothesis}[theorem]{Hypothesis}
	\if@cymraeg
		\newtheorem{definition}[theorem]{Diffiniad}
		\newtheorem{lemma}[theorem]{Lema}
		\newtheorem{proposition}[theorem]{Gosodiad}
		\newtheorem{corollary}[theorem]{Canlyneb}
		\newtheorem{remark}[theorem]{Sylwad}
		\newtheorem{example}[theorem]{Enghraifft}
		\newtheorem{exercise}[theorem]{Ymarfer}
		\newenvironment{examplecont}[1]{\textbf{Enghraifft~{#1}} (\textsl{parhad})\par}{\vspace*{2ex}}
	\else
		\newtheorem{definition}[theorem]{Definition}
		\newtheorem{lemma}[theorem]{Lemma}
		\newtheorem{proposition}[theorem]{Proposition}
		\newtheorem{corollary}[theorem]{Corollary}
		\newtheorem{remark}[theorem]{Remark}
		\newtheorem{example}[theorem]{Example}
		\newtheorem{exercise}[theorem]{Exercise}
		\newenvironment{examplecont}[1]{\textbf{Example~{#1}} (\textsl{continued})\par}{\vspace*{2ex}}
	\fi
	

	% colours
	\newcommand{\de@ShowColour}{black}
	\newcommand{\de@HideColour}{black}
	\if@blanks
		\renewcommand{\de@HideColour}{white}
	\fi
	\newcommand{\sethidecolour}[1]{\renewcommand{\de@HideColour}{#1}}
	\newcommand{\hideon}{\color{\de@HideColour}}
	\newcommand{\hideoff}{\color{\de@ShowColour}}
	\newcommand{\showboxes}{\renewcommand{\hideon}{\color{\de@ShowColour}}}
	\newcommand{\hideboxes}{\renewcommand{\hideon}{\color{\de@HideColour}}}
	\newcommand{\hide}[1]{{\hideon{{#1}}\hideoff}}

	% proof
	\newenvironment{proof}{%
		\vspace*{-3ex}\renewcommand{\solutiontitle}{\noindent\textbf{Proof:}\quad}
		\begin{TheSolution}\hideon
	}{%
		\hideoff	\end{TheSolution}
	}
	% solution
	\renewenvironment{solution}{%
		\vspace*{-3ex}\renewcommand{\solutiontitle}{\noindent\textbf{Solution:}\quad}
		\begin{TheSolution}\hideon
	}{%
		\hideoff	\end{TheSolution}
	}

	% hidebox
	\newenvironment{hidebox}{%
		\vspace*{-2ex}
		\renewcommand{\solutiontitle}{}
		\begin{TheSolution}\hideon
	}{%
		\hideoff\end{TheSolution}
	}

	
%	% headers and footers (exam.cls commands)
	\firstpageheader{}{}{}
	\runningheader{\textcolor{gray}{\scriptsize\scshape\themodulecode~Lecture~\thedocnumber}}	{}{\textcolor{gray}{\scriptsize\scshape\thedoctitle}}
	\runningheadrule
	\firstpagefooter{}{}{}
	\runningfooter{\textcolor{gray}{{\ttfamily\tiny\versionname:\ \today}}}{}{\textcolor{gray}{\scriptsize\thepage/\numpages}}
	\runningfootrule

	% counters (include doc number if defined)
%	\@ifundefined{thedocnumber}{}{\newcommand{\thedocnumber{}}}
	\renewcommand{\thesection}{\thedocnumber.\arabic{section}}
	\renewcommand{\theequation}{\thedocnumber.\arabic{equation}}
	\renewcommand{\thetheorem}{\thedocnumber.\arabic{theorem}}
	\renewcommand{\thelemma}{\thedocnumber.\arabic{lemma}}
	\renewcommand{\thedefinition}{\thedocnumber.\arabic{definition}}
	\renewcommand{\thefigure}{\thedocnumber.\arabic{figure}}
	\renewcommand{\thetable}{\thedocnumber.\arabic{table}}
	\renewcommand{\theexample}{\thedocnumber.\arabic{example}}
	\renewcommand{\theremark}{\thedocnumber.\arabic{remark}}

	% title
	\renewcommand{\maketitle}{%
		\clearpage
		\thispagestyle{empty}		
    		\vspace*{\fill}
		\fbox{\fbox{\begin{minipage}{\linewidth}\centering
		\vspace*{5ex}\par
		\ttfamily
%		\begin{tabular}{|ll|}\hline
%		\@ifundefined{themodulecode}{}{\modulecodename 		& \themodulecode \\}
%		\@ifundefined{themoduletitle}{}{\moduletitlename		& \themoduletitle \\}
%		\@ifundefined{theacademicyear}{}{\academicyearname	& \theacademicyear \\}
%		\@ifundefined{thedoctype}{}{\doctypename 			& \thedoctype \\}
%		\@ifundefined{thedoctitle}{}{\doctitlename		& \thedoctitle\\}
%		\@ifundefined{thedocnumber}{}{\docnumbername			& \thedocnumber\\}\hline
%		\end{tabular}
		\begin{tabular}{|l|}\hline
		\@ifundefined{themodulecode}{}{\themodulecode \\}
		\@ifundefined{themoduletitle}{}{\themoduletitle \\}
		\@ifundefined{theacademicyear}{}{\theacademicyear \\}
		\@ifundefined{thedoctype}{}{\thedoctype~\thedocnumber \\}
		\@ifundefined{thedoctitle}{}{\thedoctitle\\}\hline
		\end{tabular}
		\normalfont
		\vspace*{5ex}\par
		\end{minipage}}}
    		\vspace*{\fill}
		\
	}
	
	% slide breaks	
	\renewcommand{\break}{\newpage}

	% tableofcontents
	\setcounter{tocdepth}{1}
	\renewcommand*{\l@section}{\@dottedtocline{1}{1.5em}{2.3em}}
	\def\contentsname{\mbox{}\par\vspace*{0ex}\large Lecture~\thedocnumber\quad\thedoctitle}
	\let\oldtableofcontents=\tableofcontents
	\renewcommand{\tableofcontents}{\newpage\oldtableofcontents\newpage}

	% load hyperref
	\RequirePackage{hyperref}
	
	% at begin document (screws with hyperref)
	\AtBeginDocument{}

	% at end document
	\AtEndDocument{}
	
\fi

%------------------------------------------------------------------------------
% exampaper option
%------------------------------------------------------------------------------
\if@exampaper
	\typeout{------------------------------}
	\typeout{'exampaper' option detected}
	\typeout{------------------------------}

	% meta
%	\doctype{Exampaper}

	% fonts
	\RequirePackage{times}
	
%	% margins
%	\geometry{left=30mm,right=30mm,top=30mm,bottom=30mm}
	% layout (A4)
	\geometry{paperwidth=210mm, paperheight=297mm	}
	\geometry{left=30mm,right=40mm,top=30mm,bottom=30mm}
	
	% options for exam class
	\bracketedpoints
	\pointsinrightmargin
	\pointsdroppedatright
	\addpoints
	
	% tweaks of exam class
	\renewcommand{\questionshook}{\addtolength{\itemsep}{3ex}}
	\renewcommand{\labelenumi}{(\alph{enumi})}
	\renewcommand{\subpartlabel}{(\thesubpart)}
	
	% rubric info
	\RequirePackage{xstring}
	%\newcommand{\examyear}[1]{\newcommand{\theexamyear}{#1}}
	%\newcommand{\examperiod}[1]{\newcommand{\theexamperiod}{#1}}
	\newcommand{\examnumber}[1]{\newcommand{\theexamnumber}{#1}}
	\newcommand{\examtitle}[1]{\newcommand{\theexamtitle}{#1}}
	\newcommand{\duration}[1]{\newcommand{\theduration}{#1}}
	\newcommand{\appendices}[1]{\newcommand{\theappendices}{#1}}
	\newcommand{\marksinfo}[1]{\newcommand{\themarksinfo}{#1}}
	\newcommand{\maxmark}[1]{\newcommand{\themaxmark}{#1}}
	\newcommand{\percentage}[1]{\newcommand{\thepercentage}{#1}}
	\newcommand{\stationery}[1]{\newcommand{\thestationery}{#1}}
	\newcommand{\instructions}[1]{\newcommand{\theinstructions}{#1}}
	\newcommand{\examyear}[1]{%
		\newcommand{\theexamyear}{#1}
		\newcommand{\theexamyearsuffix}{\StrRight{#1}{2}}
	}
	\newcommand{\examperiod}[1]{%
		\newcommand{\theexamperiod}{#1}
		\newcommand{\theexamperiodcode}{\StrLeft{#1}{1}}
	}
	
	% choose rubric or watermark at begin document
	\AtBeginDocument{
	\ifprintanswers
		\usepackage{draftwatermark}
		\SetWatermarkLightness{0.9}
		\SetWatermarkText{SOLUTIONS}
		\SetWatermarkAngle{60}
		\renewcommand{\makerubric}{}
		\rfoot{}{}
	\else
		\makerubric
	\fi
	}
	
	% headers and footers
	\rhead{\theexamnumber/\theexamyearsuffix\theexamperiodcode}
	\cfoot{\iflastpage{\thepage X}{\thepage}}
	\rfoot{\iflastpage{END OF EXAMINATION}{PLEASE TURN OVER}}
	
	% spell out counters (in words)
	\iflastpage{\newcounter{numberofpages}\setcounter{numberofpages}{\thepage}}{}
	\newcommand{\spelled}[1]{%
	  \ifcase#1\relax\or{ONE}\or{TWO}\or{THREE}\or{FOUR}\or{FIVE}\or{SIX}\or{SEVEN}\or{EIGHT}\or{NINE}\or{TEN}\or{ELEVEN}\or{TWELVE}\or{THIRTEEN}\or{FOURTEEN}\or{FIFTEEN}\or{SIXTEEN}\or{SEVENTEEN}\or{EIGHTEEN}\or{NINETEEN}\or{TWENTY}\else{UNDEF}\fi
	}
	
	% Redefine section command (with *magic* for section count)
	\let\oldsection=\section
	\renewcommand{\section}[1]{%
		\stepcounter{numsections}
		\vspace*{2ex}
		\begin{minipage}{\linewidth}\centering
		\bfseries Section~\Alph{numsections}\\
		{({#1})}\normalfont
		\vspace*{2ex}
		\end{minipage}
	}
	\def\cuexam@numsections{0}
	\newcounter{numsections}
	\def\numsections{\@ifundefined{cuexam@numsections}%
	  {\mbox{\normalfont\bf ??}}%
	  \cuexam@numsections
	}
	\AtEndDocument{
	    \immediate\write\@auxout{%
	    	\string\gdef\string\cuexam@numsections{\thenumsections}}
	}
	
	% make rubric
	\newcommand{\makerubric}{%
	\noindent
	\hspace{-3mm}
	\begin{tabular}{ll}
	\textbf{CARDIFF UNIVERSITY} & \\
	\textbf{EXAMINATION PAPER} & \\ \\ \\ 
	\textbf{Academic Year:} & \theexamyear \\ \\
	\textbf{Examination Period:} & \theexamperiod \\ \\
	\textbf{Examination Paper Number:} & \theexamnumber \\ \\
	\textbf{Examination Paper Title:} & \theexamtitle \\ \\
	\textbf{Duration:} & \theduration \\
	\end{tabular}
	\vspace{1cm}
	
	\noindent\textbf{Do not turn this page over until instructed to do so by the Senior Invigilator.}
	\vspace{10mm}
	
	\noindent\textbf{Structure of Examination Paper:}
	\vspace{5mm}
	
	\noindent There are \spelled{\numpages}~pages.\\
	%
	\ifnum \cuexam@numsections > 1 {%
	\noindent This examination paper is divided into \spelled{\numsections}~sections.\\
	}\fi
	%
	\noindent There are \spelled{\numquestions}~questions in total. \\
	\noindent \theappendices \\
	\noindent The maximum mark for the examination paper is \themaxmark\ (\thepercentage\% of the module mark) and the mark obtainable for each question or part of a question is shown in brackets alongside the question.
	
	\vspace{5mm}
	\noindent\textbf{Students to be provided with:}
	\vspace{5mm}
	
	\noindent The following items of stationery are to be provided at the start of the examination:\\
	\thestationery\\
	\vspace{5mm}
	
	\noindent\textbf{Instructions to Students:}
	\vspace{5mm}
	
	\noindent\theinstructions
	\vfill
	
	\noindent The use of a translation dictionary between English or Welsh and another language, provided that it bears an appropriate departmental stamp, is permitted in this examination. \\
	\newpage
	}
\fi

% the end	
\endinput
