%!TEX encoding = UTF-8 Unicode filename: camel.cls
% author: scmde
% date: 28/08/2014
\NeedsTeXFormat{LaTeX2e}
\def\fileversion{1.0}
\def\filedate{2014/08/28}
\ProvidesClass{camel}[\filedate \space v\fileversion \space (scmde)]
\ProvidesFile{camel.cls}[\filedate \space v\fileversion \space (scmde)]

% options
\newif\if@cymraeg\@cymraegfalse
\newif\if@screen\@screenfalse
\newif\if@blanks\@blanksfalse
\newif\if@answers\@answersfalse
\newif\if@answersatend\@answersatendfalse

% shortcuts (to set options in preamble, rather than passing to class)
\def\printcymraeg{\@cymraegtrue} 
\def\printscreen{\@screentrue} 
\def\printblanks{\@blankstrue} 
\def\printanswers{\@answerstrue\@answersatendfalse} 
\def\printanswersatend{\@answersatendtrue\@answersfalse}

% command line options
\ifnum\interactionmode = 2
	\def\optionYes{Y}
	\def\optionNo{N}
	\ifx\cymraeg\undefined\typein[\cymraeg]{Cymraeg? (Y/N)}\fi
	\ifx\cymraeg\optionYes\@cymraegtrue\fi
	\ifx\screen\undefined\typein[\screen]{Screen? (Y/N)}\fi
	\ifx\screen\optionYes\@screentrue\fi
	\ifx\blanks\undefined\typein[\blanks]{Blanks? (Y/N)}\fi
	\ifx\blanks\optionYes\@blankstrue\fi
	\ifx\answers\undefined\typein[\answers]{Answers? (Y/N)}\fi
	\ifx\answers\optionYes\@answerstrue\@answersatendfalse\fi
	\ifx\answersatend\undefined\typein[\answersatend]{Answers at end? (Y/N)}\fi
	\ifx\answersatend\optionYes\@answersatendtrue\@answersfalse\fi
\fi

% class options
\DeclareOption{cymraeg}{\ifx\cymraeg\undefined\@cymraegtrue\else\message{^^J'cymraeg' option has no effect^^J}\fi}
\DeclareOption{screen}{\ifx\screen\undefined\@screentrue\else\message{^^J'screen' option has no effect^^J}\fi}
\DeclareOption{blanks}{\ifx\blanks\undefined\@blankstrue\else\message{^^J'blanks' option has no effect^^J}\fi}
\DeclareOption{answers}{\ifx\answers\undefined\@answerstrue\else\message{^^J'answers' option has no effect^^J}\fi}
\DeclareOption{answersatend}{\ifx\answersatend\undefined\@answersatendtrue\else\message{^^J'answersatend' option has no effect^^J}\fi}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions
\relax

% message
\message{>>>>> OPTIONS:}
\if@cymraeg\message{ CYMRAEG}\fi
\if@screen\message{ SCREEN}\fi
\if@blanks\message{ BLANKS}\fi
\if@answers\message{ ANSWERS}\fi
\if@answersatend\message{ ANSWERSATEND}\fi
\message{<<<<<}

% load class
\LoadClass[oneside]{book}

% common packages
\RequirePackage{amsmath,amsfonts}
\RequirePackage[a4paper,margin=20mm]{geometry}

% load hyperref (always load last)
%\RequirePackage{hyperref}
%\hypersetup{pdfborder = {0 0 0}}


% default fonts (for pdf)
%\renewcommand{\rmdefault}{ptm}
%\renewcommand{\sfdefault}{phv}
%\renewcommand{\ttdefault}{pcr}
%\renewcommand{\familydefault}{\rmdefault}

% GB date format
\def\today{\number\day/\number\month/\number\year}

%-------------------------------------------------
% cymraeg
%-------------------------------------------------
%\RequirePackage{comment}
%\newcommand{\cym}[1]{}
%\newcommand{\eng}[1]{{#1}}
%\newenvironment{cymraeg}{\comment}{\endcomment}
%\newenvironment{english}{}{}
%\if@cymraeg
%    \renewcommand{\cym}[1]{{#1}}
%    \renewcommand{\eng}[1]{}
%	\renewenvironment{cymraeg}{}{}
%	\renewenvironment{english}{\comment}{\endcomment}
%\fi

%-------------------------------------------------
% miscellaneous (needs to be integrated)
%-------------------------------------------------
\setlength{\parindent}{0ex}
\setlength{\parskip}{0.5ex}


\renewcommand{\chaptername}{Lecture}

\usepackage[pagestyles]{titlesec}
\usepackage{titletoc}
\setcounter{tocdepth}{1}

\titleformat{\chapter}
	{\bfseries\huge}{\chaptername~\thechapter}{1em}{}
\titleformat{\section}
	{\Large\bfseries}{\thesection}{1em}{}

\newcommand\chaptocrule{\noindent\rule[1pt]{\textwidth}{0.5pt}}
\newcommand\chapcontents{%
  \chaptocrule
  \printlist[chapters]{toc}{}{}{}\par\nobreak
  \chaptocrule\vspace*{3ex}
 }

\newpagestyle{main}[\small\scshape]{
\headrule
\sethead{\themodulecode}{}{\thechapter.~\chaptertitle} % odd
\setfoot{}{}{\thepage}
}
\newpagestyle{answers}[\small\scshape]{
\headrule
\sethead{Answers}{\themodulecode}{Answers} % odd
\setfoot{Answers}{\thepage}{}
}
\newpagestyle{exercises}[\small\scshape]{
\headrule
\sethead{\themodulecode}{}{Exercises} % odd
\setfoot{}{}{\thepage}
}
\newpagestyle{solutions}[\small\scshape]{
\headrule
\sethead{Solutions}{\themodulecode}{Solutions} % odd
\setfoot{Solutions}{\thepage}{Solutions}
}
\pagestyle{main}


\renewcommand{\labelenumi}{(\arabic{enumi})}
\renewcommand{\labelenumii}{(\alph{enumii})}

\newcommand{\makefrontmatter}{%
	\if@screen
		% do nothing
	\else
		\renewcommand{\thepage}{(\roman{page})}
		\maketitle
		\tableofcontents
		\newpage
		\setcounter{page}{1}
		\renewcommand{\thepage}{\arabic{page}}
	\fi
}


%-------------------------------------------------
% module information
%-------------------------------------------------
\newcommand{\academicyear}[1]{\newcommand{\theacademicyear}{#1}}
\newcommand{\modulecode}[1]{\newcommand{\themodulecode}{#1}}
\newcommand{\moduletitle}[1]{\newcommand{\themoduletitle}{#1}}
\newcommand{\booktitle}[1]{\newcommand{\thebooktitle}{#1}}

% names
\newcommand{\academicyearname}{Year}
\newcommand{\modulecodename}{Code}
\newcommand{\modulename}{Module}
\newcommand{\versionname}{Version}
\newcommand{\instructionsname}{Instructions}
\newcommand{\exercisesname}{Exercises}
\newcommand{\exercisename}{Exercise}
\newcommand{\questionsname}{Questions}
\newcommand{\questionname}{Question}
\newcommand{\answersname}{Answers}
\newcommand{\answername}{Answer}
\newcommand{\solutionname}{Solution}
\newcommand{\proofname}{Proof}
\if@cymraeg
	\renewcommand{\academicyearname}{Blwyddyn}
	\renewcommand{\modulename}{Modiwl}
	\renewcommand{\modulecodename}{C\^{o}d}
	\renewcommand{\instructionsname}{Cyfarwyddiadau}
	\renewcommand{\exercisesname}{Ymarferion}
	\renewcommand{\exercisename}{Ymarfer}
    \newcommand{\questionsname}{Cwestiynnau}
    \newcommand{\questionname}{Cwestiwn}
	\renewcommand{\answersname}{Atebion}
	\renewcommand{\answername}{Ateb}
	\renewcommand{\solutionname}{Datrysiad}
	\newcommand{\proofname}{Prawf}
\fi	

% theorem names
\newcommand{\theoremnamex}{Theorem}
\newcommand{\lemmanamex}{Lemma}
\newcommand{\hypothesisnamex}{Hypothesis}
\newcommand{\propositionnamex}{Proposition}
\newcommand{\corollarynamex}{Corollary}
\newcommand{\conjecturenamex}{Conjecture}
\newcommand{\algorithmnamex}{Algorithm}
\newcommand{\definitionnamex}{Definition}
\newcommand{\remarknamex}{Remark}
\newcommand{\problemnamex}{Problem}
\newcommand{\notenamex}{Note}
\newcommand{\notationnamex}{Notation}
\newcommand{\claimnamex}{Claim}
\newcommand{\summarynamex}{Summary}
\newcommand{\conclusionnamex}{Conclusion}
\newcommand{\examplenamex}{Example}
\if@cymraeg
	\renewcommand{\lemmanamex}{Lema}
	\renewcommand{\propositionnamex}{Proposition}
	\renewcommand{\corollarynamex}{Canlyneb}
	\renewcommand{\conjecturex}{Gosodiad}
	\renewcommand{\algorithmx}{Algorithm}
	\renewcommand{\definitionnamex}{Definition}
	\renewcommand{\remarknamex}{Sylwad}
	\renewcommand{\notenamex}{Nodyn}
	\renewcommand{\notationnamex}{Nodiant}
	\renewcommand{\claimnamex}{Honiad}
	\renewcommand{\summarynamex}{Crynodeb}
	\renewcommand{\conclusionnamex}{Casgliad}
	\renewcommand{\examplenamex}{Enghraifft}
\fi

%-------------------------------------------------
% common settings (paper version)
%-------------------------------------------------

\newcommand{\spar}{\if@screen\par\fi}

% dummy commands
\renewcommand{\break}{}

% steps (used with show/hide)
\newenvironment{steps}{\begin{enumerate}}{\end{enumerate}}
\newcommand{\step}[1]{\item {{#1}}}

% theorems
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage[hyperref, thmmarks, amsmath]{ntheorem}

\theoremstyle{break}
\setlength\theorempreskipamount{4ex}
\setlength\theorempostskipamount{2ex}
\theorembodyfont{\upshape}
\qedsymbol{\rule{1ex}{1ex}}

\newcounter{theorem}[chapter]
\newtheorem{theorem}{\theoremnamex}
\newtheorem{lemma}[theorem]{\lemmanamex}
\newtheorem{proposition}[theorem]{\propositionnamex}
\newtheorem{corollary}[theorem]{\corollarynamex}
\newtheorem{conjecture}[theorem]{\conjecturenamex}
\newtheorem{hypothesis}[theorem]{\hypothesisnamex}
\newtheorem{algorithm}[theorem]{\algorithmnamex}

\newtheorem{definition}[theorem]{\definitionnamex}
\newtheorem{problem}[theorem]{\problemnamex}
\newtheorem{example}[theorem]{\examplenamex}

\newtheorem{remark}[theorem]{\remarknamex}
\newtheorem{note}[theorem]{\notenamex}
\newtheorem{notation}[theorem]{\notationnamex}
\newtheorem{claim}[theorem]{\claimnamex}
\newtheorem{summary}[theorem]{\summarynamex}
\newtheorem{conclusion}[theorem]{\conclusionnamex}


%-------------------------------------------------
% boxes
%\RequirePackage[framemethod=TikZ]{mdframed}
\RequirePackage{mdframed}
\RequirePackage{xcolor}

% set show/hide colours
\newcommand{\de@ShowColour}{black}
\newcommand{\de@HideColour}{black}
\newcommand{\sethidecolour}[1]{\renewcommand{\de@HideColour}{#1}}
\newcommand{\hideon}{\color{\de@HideColour}}
\newcommand{\hideoff}{\color{\de@ShowColour}}
\newcommand{\hide}[1]{{\hideon{{#1}}\hideoff}}
\if@blanks
	\renewcommand{\de@HideColour}{white}
\fi

\RequirePackage{tcolorbox}
\tcbuselibrary{breakable}

% proof
\newcommand{\prooftitle}{\noindent\textbf{\proofname:}\enspace}
\newenvironment{proof}{%
	\vspace{\parskip}
	\begin{tcolorbox}[breakable,notitle,boxrule=0.5pt,colback=white,coltext=\de@HideColour]
%	\begin{mdframed}%[linecolor=red]
	\textcolor{\de@ShowColour}{\prooftitle}
	\begingroup
	\hideon
}{%
	\hideoff
	\endgroup	
    \end{tcolorbox}
%	\end{mdframed} 
}

% solution
\newcommand{\solutiontitle}{\noindent\textbf{\solutionname:}\enspace}
\newenvironment{solution}{%
	\vspace{\parskip}
	\begin{tcolorbox}[breakable,notitle,boxrule=0.5pt,colback=white,coltext=\de@HideColour]
%	\begin{mdframed}%[linecolor=red]
	\textcolor{\de@ShowColour}{\solutiontitle}
	\hideon
}{%
	\hideoff	
    \end{tcolorbox}
%	\end{mdframed} 
}
%\surroundwithmdframed[linewidth=2pt]{proof}
%\newmdenv[linecolor=red,frametitle=Proof:]{proof}


% hidebox
\newenvironment{hidebox}{%
	\begin{tcolorbox}[breakable,notitle,boxrule=0.5pt,colback=white,coltext=\de@HideColour]
%	\begin{mdframed}
	\hideon
}{%
	\hideoff
%	\end{mdframed}
    \end{tcolorbox}
}

%-------------------------------------------------
% titles
\renewcommand{\maketitle}{%
    \thispagestyle{empty}
	\begin{center}
		\scshape
		\Large Cardiff University \hfill School of Mathematics \\[10ex]
		\huge \themodulecode \\ [7ex]
		\huge \themoduletitle \\[8ex]
		\huge \@ifundefined{thebooktitle}{Lecture Notes}{\thebooktitle} \\[8ex]
		\huge \theacademicyear 
	\end{center}
	\vfill
	\normalsize
	\raggedleft
	\texttt{Version: \today}
	\flushleft
	\normalsize
	\newpage
}

% custom chapter name
%\renewcommand{\@makechapterhead}[1]{%
%	\vspace*{2ex}\Large
%	\textsc{\themodulecode~Lecture~\thechapter\hfill #1\mbox{}}
%	\normalsize\vspace*{2ex}
%}
%\renewcommand{\@makechapterhead}[1]{}

%-------------------------------------------------
% counters
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
\renewcommand{\thetheorem}{\thechapter.\arabic{theorem}}
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}


%-------------------------------------------------
% exercises
\RequirePackage{xifthen} % provides \isempty test
\newcounter{exercise}[chapter]
\renewcommand{\theexercise}{\thechapter.\arabic{exercise}}

%\newcounter{exe}[section]
%\renewcommand{\theexe}{\thesection.\arabic{exe}}

% exercise
\newcommand{\exercisetitle}{}
\newenvironment{exercise}[1][]{%
  \refstepcounter{exercise}
%  \stepcounter{exe}
  \ifthenelse{\isempty{#1}}{\renewcommand{\exercisetitle}{}}{\renewcommand{\exercisetitle}{\space[#1]}}
%  \renewcommand{\exercisename}{Ymarfer \theexercise\quad\exercisetitle}
  \renewcommand{\exercisename}{Exercise \theexercise\quad\exercisetitle}
  \par\vspace{2ex}\noindent\textbf{\exercisename\normalsize} \par
  \ans@write{\noexpand\subsection*{\exercisename}}
}{}

% diagnostic/formative/summative
\newenvironment{diagnostic}{\begin{exercise}[Diagnositic]}{\end{exercise}}
\newenvironment{formative}{\begin{exercise}[Formative]}{\end{exercise}}
\newenvironment{summative}{\begin{exercise}[Summative]}{\end{exercise}}

\RequirePackage{fancyvrb}
\newenvironment{ateb}
	{\VerbatimOut{\jobname.ateb}}
	{\endVerbatimOut}

% answer
\newcommand{\answertitle}{\noindent\textbf{\answername:}\enspace}
\RequirePackage{environ}

%\NewEnviron{answer}{%
%    \if@answers%
%        \vspace*{\parskip}%
%        \begin{minipage}{\linewidth}
%        \begin{mdframed}[backgroundcolor=gray!10]%
%        \answertitle%
%        \BODY%
%        \end{mdframed}%
%		\end{minipage}
%    \fi%
%    \if@answersatend
%		\ans@write{\BODY}%
%	\fi
%}{}
%
%

%\newcounter{answerno}
\NewEnviron{answer}{%
%	\stepcounter{answerno}
    \if@answers%
    	\par\vspace*{3ex}
%		\par\vspace*{\parskip}%
%        \begin{minipage}{\linewidth}
%        \begin{mdframed}[backgroundcolor=gray!10]%
%        \begin{mdframed}[backgroundcolor=gray!5]%
%        \begin{mdframed}[backgroundcolor=white]%
%		\hrule
		\begin{tcolorbox}[breakable,notitle,boxrule=0pt,colback=blue!10,colframe=blue!20]
        \answertitle%
        \BODY%
        \end{tcolorbox}
%        \hrule
%        \end{mdframed}%
		\par\vspace*{\parskip}%
%		\end{minipage}
    \fi%
    \if@answersatend
%    	\edef\cynnwys{\noexpand\BODY}
		\gdef\tmpname{ans\Roman{answerno}}
		\typeout{\tmpname}
%		\immediate\protected@write\@ansout{}{\protect\csname\tmpname\endcsname}
		\immediate\write\@ansout{\csname\tmpname\endcsname}
		\expandafter\gdef\csname\tmpname\endcsname{dingding}
	\fi
}{}



% shortcut for write to answers file
\def\ans@write#1{
    \immediate\write\@ansout{#1}
%	\let\protect\string
%	\protected@iwrite{#1}
}
%\newcommand{\ans@write}[1]{\immediate\write\@ansout{{#1}}}

%-------------------------------------------------
% print-answers-at-end

%\let\oldsection=\section
%\renewcommand{\section}{\break\oldsection}

%\let\oldchapter=\chapter
%\renewcommand{\chapter}[1]{\oldchapter{#1}\dominitoc\minitoc}

% open answers file at beginning
\AtBeginDocument{
    \ifx\@undefined\@ansout\newwrite\@ansout\fi
    \immediate\openout\@ansout=\jobname.ans
%    \if@answersatend
%    	\Opensolutionfile{zzz}
%	\fi
}
% close and process input answers file at end 
\AtEndDocument{
	\immediate\closeout\@ansout
	\if@answersatend
%		\Closesolutionfile{zzz}
%		\Readsolutionfile{zzz}
		\typeout{Now typesetting answers ....}
	    \cleardoublepage
	    \setcounter{page}{1}
	    \appendix
		\renewcommand{\@makechapterhead}[1]{%
			\thispagestyle{answers}
			\vspace*{2ex}
			\begin{center}
			\Huge\textbf{Answers to Exercises}\normalsize
			\end{center}
			\vspace*{4ex}
		}
	    \chapter{Answers}
	    \pagestyle{answers}
		\renewcommand{\labelenumi}{\arabic{enumi}.}
		\renewcommand{\labelenumii}{(\alph{enumii})}
		\renewcommand{\labelenumiii}{(\roman{enumiii})}
		\renewcommand{\labelenumiv}{\alph{enumiv}}
		\input{\jobname.ans}
	\fi
}


%\RequirePackage{verbatim}
%\long\def\protected@iwrite#1#2#3{%
%  \begingroup
%    \let\thepage\relax
%    #2%
%    \let\protect\@unexpandable@protect
%    \edef \reserved@a{\immediate\write#1{#3}}%
%    \reserved@a
%  \endgroup
%  \if@nobreak
%    \ifvmode
%      \nobreak
%    \fi
%  \fi
%}

%\RequirePackage{verbatim}
%\long\def\protected@iwrite#1{%
%  \begingroup
%    \let\thepage\relax
%    \let\protect\@unexpandable@protect
%    \edef \reserved@a{\immediate\write\@ansout{#1}}%
%    \reserved@a
%  \endgroup
%  \if@nobreak
%    \ifvmode
%      \nobreak
%    \fi
%  \fi
%}


%-------------------------------------------------
% screen option (override paper options defined above)
%-------------------------------------------------
\if@screen

	% slide breaks	
%	\let\oldnewpage=\newpage
%	\renewcommand{\break}{\oldnewpage}
%	\renewcommand{\newpage}{}
	\renewcommand{\break}{\newpage}
	
	% fonts
	\renewcommand{\familydefault}{\sfdefault}
	\usepackage[T1]{fontenc}
	\usepackage{lmodern}
	\usepackage{exscale} 
	\usepackage{scrextend}
	\changefontsizes{18pt}
	
	\renewcommand\baselinestretch{1.1}
	\setlength{\parskip}{0.5ex}

	% layout (A4 landscape)
%	\geometry{paperwidth=297mm, paperheight=210mm	}
	\geometry{left=15mm,right=15mm,top=18mm,bottom=18mm}
	\geometry{a4paper,landscape}
	
	% spacing
	\setlength{\parindent}{0ex}
	\addtolength{\topskip}{4ex}
	\addtolength{\tabcolsep}{1ex}
	\renewcommand{\arraystretch}{1.3}
	\addtolength{\arraycolsep}{0.5ex}

	% custom itemize 
	\renewenvironment{itemize}{%
	\begin{list}{$\bullet$\ }{%
	    \setlength{\itemsep}{0ex plus 0.2ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	    \setlength{\topsep}{1ex}
	}}{\end{list}}
	
	% custom enumerate
	\renewenvironment{enumerate}{%
	\begin{list}{(\arabic{enumi})}{%
	    \usecounter{enumi}
	    \setlength{\itemsep}{0.25ex plus 0.15ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	}} {\end{list}}

	% custom chapter name
%	\renewcommand{\@makechapterhead}[1]{%
%		\setcounter{page}{1}
%		\thispagestyle{empty}
%		\small
%%		\textsc{\themodulecode~\themoduletitle\hfill\theacademicyear\mbox{}}\par
%		\textsc{\themodulecode~\themoduletitle}\par
%		\normalsize
%		\vspace*{7ex}
%		\large
%		\textsc{Lecture~\thechapter.~ #1}
%		\normalsize
%		\vspace*{2ex}
%	}
	
\fi


%-------------------------------------------------
% headers and footers (can't override paper settings for screen)
%-------------------------------------------------
%\RequirePackage{fancyhdr}
%\fancyhf{}
%\pagestyle{fancy}
%\if@screen
%	\addtolength{\headheight}{1ex}
%    \renewcommand{\headrulewidth}{0.01pt}
%	\fancyhead[L]{\footnotesize\scshape\nouppercase\leftmark}
%    \fancyfoot[R]{\footnotesize\scshape\thepage}
%\else
%	\renewcommand{\headrulewidth}{0.01pt}
%	\fancyhead[L]{\small\scshape\nouppercase\leftmark}
%	\fancyhead[C]{\small\scshape\themodulecode}
%	\fancyhead[R]{\small\scshape\nouppercase\rightmark}
%	\fancyfoot[C]{\small\thepage}
%\fi
%% answers page style
%\fancypagestyle{answers}{
%	\fancyhf{}
%	\renewcommand{\headrulewidth}{0pt}
%	\fancyhead[L,R]{ANSWERS}
%	\fancyhead[C]{\scshape\themodulecode}
%	\fancyfoot[L,R]{ANSWERS}
%	\fancyfoot[C]{(\thepage)}
%}



%------------------------------------------------
% exam.cls rip-off starts here
%------------------------------------------------

% counters
\newcounter{question}
\newcounter{partno}
\newcounter{subpart}
\newcounter{subsubpart}
\newcounter{choice}

% hooks (for user customization)
\newcommand\questionshook{}
\newcommand\partshook{}
\newcommand\subpartshook{}
\newcommand\subsubpartshook{}
\newcommand\choiceshook{}
\newcommand\checkboxeshook{}

%--------------------
% questions
\newenvironment{questions}{%
%  \Writetofile{zzz}{\noexpand\begin{enumerate}}
%  \Writetofile{zzz}{\noexpand\subsection*{\thechapter.\theexercise.\thequestion}}
  \ans@write{\noexpand\begin{enumerate}}
  \def\@queslevel{question}%
  \def\question{%
    \ans@write{\noexpand\item}
    \def\thequestiontitle{\questionname~thequestion}%
    \@checkqueslevel{question}%
    \edef\@queslabel{question.\arabic{chapter}.\arabic{exercise}.\arabic{question}}%
    \gdef\@currentlabel{\@queslabel}%
    \label{\@queslabel}%
    \item
%  	\Writetofile{zzz}{\noexpand\subsubsection*{\thechapter.\theexercise.\thequestion}}
  } % end question
  \def\subpart{%
    \ans@write{\noexpand\item}
    \@checkqueslevel{subpart}%
    \edef\@subpartlabel{subpart.\arabic{question}.\arabic{partno}.\arabic{subpart}}%
    \label{\@subpartlabel}%
    \item
  } % end subpart
  \def\subsubpart{%
    \ans@write{\noexpand\item}
    \@checkqueslevel{subsubpart}%
    \edef\@subsubpartlabel{subsubpart.\arabic{question}.\arabic{partno}.\arabic{subpart}.\arabic{subsubpart}}
    \label{\@subsubpartlabel}%
    \item
  } % end subsubpart 
  \list{\question@number}{%
    \usecounter{question}%
    \settowidth{\leftmargin}{10.\hskip\labelsep}%
    \labelwidth\leftmargin\advance\labelwidth-\labelsep
    \partopsep=0pt
    \questionshook
    }%
}{%
	\endlist
	\ans@write{\noexpand\end{enumerate}}
%	\Writetofile{zzz}{\noexpand\end{enumerate}}
}% end questions environment
  
\def\question@number{\questionlabel}
\newcommand\questionlabel{\thequestion.}

%--------------------
% parts
\newenvironment{parts}{%
	\ans@write{\noexpand\begin{enumerate}}
%	\Writetofile{zzz}{\noexpand\begin{enumerate}}
	\def\@queslevel{part}%
	\def\part{%
    	\ans@write{\noexpand\item}
    	\@checkqueslevel{part}%
    	\edef\@partlabel{part.\arabic{chapter}.\arabic{exercise}.\arabic{question}.\arabic{partno}}%
    	\label{\@partlabel}%
    	\item
	} % end part
	\list{\partlabel}{%
    	\usecounter{partno}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{(m)\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\partshook
	}%
}{%
	\endlist
	\ans@write{\noexpand\end{enumerate}}
%	\Writetofile{zzz}{\noexpand\end{enumerate}}
} % end parts environmen

\newcommand\partlabel{\thepartno}
\def\thepartno{(\alph{partno})}

%--------------------
% subparts
\newenvironment{subparts}{%
	\ans@write{\noexpand\begin{enumerate}}
	\def\@queslevel{subpart}%
	\list{\subpartlabel}{%
    	\usecounter{subpart}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{vii.\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\subpartshook
    }%
}{%
	\endlist 
	\ans@write{\noexpand\end{enumerate}}
}

\newcommand\subpartlabel{\thesubpart}
\def\thesubpart{(\roman{subpart})}

%--------------------
% subsubparts
\newenvironment{subsubparts}{%
	\ans@write{\noexpand\begin{enumerate}}
	\def\@queslevel{subsubpart}%
	\list{\subsubpartlabel}{%
	    \usecounter{subsubpart}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{($\psi$)\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\subsubpartshook
    }%
}{%
	\endlist 
	\ans@write{\noexpand\end{enumerate}}
}

\newcommand\subsubpartlabel{\thesubsubpart.}
\def\thesubsubpart{\alph{subsubpart}}

%-----------------------
% validation
\def\@checkqueslevel#1{%
  \begingroup
    \def\@temp{#1}%
    \ifx\@temp\@queslevel
      % do nothing.
    \else
      \ClassError{exam}{%
        I found a #1 where I expected to find a \@queslevel
        \MessageBreak
      }{%
        Both #1 and \@queslevel \space can be used only inside the correct 
        \MessageBreak \space \space
        environment and outside of any smaller environment
        \MessageBreak
      }%
    \fi
  \endgroup
}

%-----------------------
% choices
\renewcommand\thechoice{\Alph{choice}.}
\newcommand\choicelabel{\thechoice}
\newif\if@correctchoice
\@correctchoicefalse
\newcommand\CorrectChoiceEmphasis[1]{%
  \def\CorrectChoice@Emphasis{#1}%
}
\CorrectChoiceEmphasis{\bfseries}
\let\correctchoiceemphasis\CorrectChoiceEmphasis

% begin choices
\newenvironment{choices}{%
	\list{\choicelabel}{%
		\usecounter{choice}\def\makelabel##1{\hss\llap{##1}}%
		\settowidth{\leftmargin}{W.\hskip\labelsep}%
       	\def\choice{%
       		\if@correctchoice
           		\endgroup
         	\fi
         	\item
		} % end choice
		\def\CorrectChoice{%
			\if@correctchoice
       			\endgroup
       		\fi
       		\if@answers
				\begingroup 
                \@correctchoicetrue
				\CorrectChoice@Emphasis
			\fi
			\item
			\if@answersatend
        		\ans@write{\thechoice}
			\fi
		} % end CorrectChoice
		\let\correctchoice\CorrectChoice
       	\topsep=2pt
       	\partopsep=0pt
       	\choiceshook
	}
}{%
	\if@correctchoice 
		\endgroup 
	\fi 
	\endlist
} % end choices

%-----------------------
% checkboxes
\RequirePackage{amssymb}
\newcommand{\checkboxchar}[1]{\def\checkbox@char{#1}}
\newcommand{\checkedchar}[1]{\def\checked@char{#1}}
\checkboxchar{$\square$}
\checkedchar{$\checkmark$}

% begin checkboxes
\newenvironment{checkboxes}%
  {\list{\checkbox@char}%
     {\usecounter{choice}%
       \settowidth{\leftmargin}{W.\hskip\labelsep}%
       \def\choice{%
         \if@correctchoice
           \endgroup
         \fi
         \item
       } % choice
       \def\CorrectChoice{%
         \if@correctchoice
           \endgroup
         \fi
         \if@answers
           \begingroup 
           \@correctchoicetrue
           \CorrectChoice@Emphasis
           \item[\checked@char]
         \else
           \item
         \fi
         \if@answersatend
            \ans@write{\thechoice}
         \fi
       } % CorrectChoice
       \let\correctchoice\CorrectChoice
       \topsep=2pt
       \partopsep=0pt
       \checkboxeshook
     }%
}{%
    \if@correctchoice 
        \endgroup 
    \fi 
    \endlist
} % enc checkboxes

%-----------------------
% move up one level
\long\def\uplevel#1{%
  \par\bigskip
  \vbox{%
    \leftskip=\@totalleftmargin
    \advance\leftskip-\leftmargin
    \advance\@totalleftmargin-\leftmargin
    \advance\linewidth\leftmargin
    #1%
  }% vbox
  \nobreak
}

%------------------------------------------------
% the end	
\endinput
%------------------------------------------------
