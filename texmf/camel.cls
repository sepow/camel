% filename: camel.cls
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
\def\printanswers{\@answerstrue} 
\def\printanswersatend{\@answersatendtrue}

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
	\ifx\answers\optionYes\@answerstrue\fi
	\ifx\answersatend\undefined\typein[\answersatend]{Answers at end? (Y/N)}\fi
	\ifx\answeratends\optionYes\@answersatendtrue\fi
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
%\message{>>>>> OPTIONS:}
%\if@cymraeg\message{ CYMRAEG}\fi
%\if@screen\message{ SCREEN}\fi
%\if@blanks\message{ BLANKS}\fi
%\if@answers\message{ ANSWERS}\fi
%\message{<<<<<}

% load class
\LoadClass[oneside]{book}

% common packages
\RequirePackage{amsmath,amsfonts}
\RequirePackage{xcolor}
\RequirePackage[a4paper,margin=20mm]{geometry}
\RequirePackage{framed}

% load hyperref (always load last)
\RequirePackage{hyperref}
\hypersetup{pdfborder = {0 0 0}}


% default fonts (for pdf)
\renewcommand{\rmdefault}{ptm}
\renewcommand{\sfdefault}{phv}
\renewcommand{\ttdefault}{pcr}
\renewcommand{\familydefault}{\rmdefault}

% GB date format
\def\today{\number\day/\number\month/\number\year}

%-------------------------------------------------
% cymraeg
%-------------------------------------------------
\RequirePackage{comment}
\newcommand{\cym}[1]{}
\newcommand{\eng}[1]{{#1}}
\newenvironment{cymraeg}{\comment}{\endcomment}
\newenvironment{english}{}{}
%\if@cymraeg
%	\typeout{camel.cls: cymraeg}
%    \renewcommand{\cym}[1]{{#1}}
%    \renewcommand{\eng}[1]{}
%	\renewenvironment{cymraeg}{}{}
%	\renewenvironment{english}{\comment}{\endcomment}
%\fi

%-------------------------------------------------
% module information
%-------------------------------------------------
\newcommand{\academicyear}[1]{\newcommand{\theacademicyear}{#1}}
\newcommand{\modulecode}[1]{\newcommand{\themodulecode}{#1}}
\newcommand{\moduletitle}[1]{\newcommand{\themoduletitle}{#1}}

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
\fi	

%-------------------------------------------------
% paper version (default)
%-------------------------------------------------

% steps (used with show/hide)
\newenvironment{steps}{\begin{enumerate}}{\end{enumerate}}
\newcommand{\step}[1]{\item {{#1}}}

% headers and footers
\RequirePackage{fancyhdr}
\pagestyle{fancy} 
\renewcommand{\chaptermark}[1]{\markboth{\textsc{\thechapter.\ \ #1}}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ #1}{}}
\renewcommand\headrulewidth{0.02pt}
\renewcommand\footrulewidth{0pt}
\addtolength{\headheight}{2pt}
\addtolength{\headsep}{5pt}
\fancyhf{}
\fancyhead[L]{\small\scshape\leftmark}
\fancyhead[R]{\small\scshape\rightmark}
\fancyfoot[C]{\small\thepage}

%\RequirePackage{fancyhdr}
%\fancyhf{}
%\renewcommand{\headrulewidth}{0pt}
%\chead{\scshape\themodulecode\quad\themoduletitle\quad\theacademicyear}
%\cfoot{{\thepage}}
%\pagestyle{fancy}

% theorem names
\newcommand{\theoremname}{Theorem}
\newcommand{\lemmaname}{Lemma}
\newcommand{\propositionname}{Proposition}
\newcommand{\corollaryname}{Corollary}
\newcommand{\conjecturename}{Conjecture}
\newcommand{\algorithmname}{Algorithm}
\newcommand{\definitionname}{Definition}
\newcommand{\remarkname}{Remark}
\newcommand{\problemname}{Problem}
\newcommand{\notename}{Note}
\newcommand{\notationname}{Notation}
\newcommand{\claimname}{Claim}
\newcommand{\summaryname}{Summary}
\newcommand{\conclusionname}{Conclusion}
\newcommand{\examplename}{Example}
\if@cymraeg
	\renewcommand{\lemmaname}{Lema}
	\renewcommand{\propositionname}{Proposition}
	\renewcommand{\corollaryname}{Canlyneb}
	\renewcommand{\conjecture}{Gosodiad}
	\renewcommand{\algorithm}{Algorithm}
	\renewcommand{\definitionname}{Definition}
	\renewcommand{\remarkname}{Sylwad}
	\renewcommand{\notename}{Nodyn}
	\renewcommand{\notationname}{Nodiant}
	\renewcommand{\claimname}{Honiad}
	\renewcommand{\summaryname}{Crynodeb}
	\renewcommand{\conclusionname}{Casgliad}
	\renewcommand{\examplename}{Enghraifft}
\fi

% theorems
\RequirePackage{amsmath,amsfonts,amssymb,amsthm}

\theoremstyle{plain}
\newtheorem{theorem}{\theoremname}
\newtheorem{lemma}[theorem]{\lemmaname}
\newtheorem{proposition}[theorem]{\propositionname}
\newtheorem{corollary}[theorem]{\corollaryname}
\newtheorem{conjecture}[theorem]{\conjecturename}
\newtheorem{algorithm}[theorem]{\algorithmname}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{\definitionname}
\newtheorem{problem}[theorem]{\problemname}
\newtheorem{example}[theorem]{\examplename}

\theoremstyle{remark}
\newtheorem{remark}[theorem]{\remarkname}
\newtheorem{note}[theorem]{\notename}
\newtheorem{notation}[theorem]{\notationname}
\newtheorem{claim}[theorem]{\claimname}
\newtheorem{summary}[theorem]{\summaryname}
\newtheorem{conclusion}[theorem]{\conclusionname}

% colours (for blank boxes)
\newcommand{\de@ShowColour}{black}
\newcommand{\de@HideColour}{black}
\newcommand{\sethidecolour}[1]{\renewcommand{\de@HideColour}{#1}}
\newcommand{\hideon}{\color{\de@HideColour}}
\newcommand{\hideoff}{\color{\de@ShowColour}}
\newcommand{\showboxes}{\renewcommand{\hideon}{\color{\de@ShowColour}}}
\newcommand{\hideboxes}{\renewcommand{\hideon}{\color{\de@HideColour}}}
\newcommand{\hide}[1]{{\hideon{{#1}}\hideoff}}
\if@blanks
	\renewcommand{\de@HideColour}{white}
\fi

% hidebox
\newenvironment{hidebox}{%
	\begin{framed}\hideon
}{%
	\hideoff\end{framed}
}

% title of book 
\renewcommand{\maketitle}{%
	\thispagestyle{empty}
    \hrule\vspace{0.25ex}\hrule\vspace{1ex}
	\noindent
	\ttfamily
	\@ifundefined{themodulecode}{}{\themodulecode} \\
    \@ifundefined{themoduletitle}{}{\themoduletitle} \\
    \@ifundefined{theacademicyear}{}{\theacademicyear}
	\normalsize\normalfont
	\vspace{0.5ex}\hrule\vspace{0.25ex}\hrule\vspace{3ex}
}

%-------------------------------------------------
% screen option (override paper options defined above)
%-------------------------------------------------
\if@screen

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
	
	% spacing
	\setlength{\parindent}{0ex}
	\addtolength{\topskip}{4ex}
	\addtolength{\tabcolsep}{1ex}
	\renewcommand{\arraystretch}{1.3}
	\addtolength{\arraycolsep}{0.5ex}

    % headers and footers (not happy!)
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhead[LO,RE]{\nouppercase{\themodulecode~\themoduletitle~\theacademicyear}}
    \fancyfoot[LO,RE]{\thepage}
    \pagestyle{fancy}

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

	% title
	\renewcommand{\maketitle}{%
		\clearpage
		\thispagestyle{empty}		
    	\vspace*{\fill}
		\fbox{\fbox{\begin{minipage}{\linewidth}\centering
		\vspace*{5ex}\par
		\ttfamily
		\begin{tabular}{|l|}\hline
		\@ifundefined{themodulecode}{}{\themodulecode \\}
		\@ifundefined{themoduletitle}{}{\themoduletitle \\}
		\@ifundefined{theacademicyear}{}{\theacademicyear \\}
		\end{tabular}
		\normalfont
		\vspace*{5ex}\par
		\end{minipage}}}
    	\vspace*{\fill}
	}
	
	% slide breaks	
	\renewcommand{\break}{\newpage}

	% fancy tableofcontents
	%\setcounter{tocdepth}{1}
	%\renewcommand*{\l@section}{\@dottedtocline{1}{1.5em}{2.3em}}
	%\def\contentsname{\mbox{}\par\vspace*{0ex}\large Lecture~\thedocnumber\quad\thedoctitle}
	%\let\oldtableofcontents=\tableofcontents
	%\renewcommand{\tableofcontents}{\newpage\oldtableofcontents\newpage}
\fi


%-------------------------------------------------
% exercises: diagnostic, formative, summative
% ripped off exam.cls
%-------------------------------------------------

% open answers file at begin document
\AtBeginDocument{
    \ifx\@undefined\@ansout\newwrite\@ansout\fi
    \immediate\openout\@ansout=\jobname.ans
}
% close and process input answers file at end document
\AtEndDocument{
	\immediate\closeout\@ansout
    \newpage
    \appendix
    \chapter{Answers}
	\renewcommand{\labelenumi}{\arabic{enumi}.}
	\renewcommand{\labelenumii}{(\alph{enumii})}
	\renewcommand{\labelenumiii}{(\roman{enumiii})}
	\renewcommand{\labelenumiv}{\alph{enumiv}}
	\input{\jobname.ans}
}

% command to write to answers file
\def\ans@write#1{
    \immediate\write\@ansout{#1}
}

% counter
\newcounter{exercise}[chapter]

% answer 
\newcommand{\answertitle}{\noindent\textbf{\answername:}\enspace}
\RequirePackage{environ}
\NewEnviron{answer}{%
    \if@answers
        \vspace{\parskip}
        \begin{framed}
        \answertitle
        \BODY
        \end{framed}
    \fi
    \if@answersatend
        \ans@write{\BODY}
    \fi
}{}

% exercise
\RequirePackage{xifthen} % provides \isempty test
\newcommand{\exercisetitle}{}
\newenvironment{exercise}[1][]{%
  \refstepcounter{exercise}
  \ifthenelse{\isempty{#1}}{\renewcommand{\exercisetitle}{}}{\renewcommand{\exercisetitle}{\space[#1]}}
  \renewcommand{\exercisename}{Exercise \thechapter.\theexercise\quad\exercisetitle}
  \par\vspace{2ex}\noindent\textbf{\large\exercisename\normalsize} \par\vspace{1ex}
  \ans@write{\noexpand\subsection*{\exercisename}}
}{}

% diagnostic
\newenvironment{diagnostic}{%
  \begin{exercise}[Diagnositic]
}{
  \end{exercise}
}
% formative 
\newenvironment{formative}{%
  \begin{exercise}[Formative]
}{%
  \end{exercise}
}
% summative
\newenvironment{summative}{%
  \begin{exercise}[Summative]
}{%
  \end{exercise}
}

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
}% end questions environment
  
\def\question@number{\questionlabel}
\newcommand\questionlabel{\thequestion.}

%--------------------
% parts
\newenvironment{parts}{%
	\ans@write{\noexpand\begin{enumerate}}
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

\newcommand\subpartlabel{\thesubpart.}
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
