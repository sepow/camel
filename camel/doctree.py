#!/usr/bin/python
'''
doctree.py: build document tree from latex file (camel.cls)

    1. latex file -> doc_tree
    2. doc_tree -> django models -> database objects
    3. doc_tree -> xml

    #--------------------
    General
    #--------------------
    LatexType: Division, Theorem, List, Item, Exercise, Label, Reference
    LatexName: Chapter, Itemize, Question, Diagnostic, 
    
    #--------------------
    Labels using materialized paths
    #--------------------
    Node.mpath is a string in the form 
    
    .001                book 1
    .001.001                chapter 1
    .001.002                chapter 2
    .001.002.001                section 1
    .001.002.002                section 2
    .001.002.003                section 3
    .001.003                 chapter 3
    
    Labels stored in a dictionary {text_label: 001.002.007.002.003}
    References implemented as {url: mpath(label)} or similar

    #--------------------
    Labels
    #--------------------
    A label should be for a database object (e.g. chapter, figure, question)
    When we encounter a label, it should be attached to the corresponding object
    A ref will then refer to the database object; the ref will be replaced by a hyperlink
    which links to the corresponding object (which can be served via its view

      label:  <a name="anchor"></a>
      ref:    <a href="#anchor">Link text</a>
              <a href="http://example..com/path/to/filename.html#anchor">Link Text</a>
    exammple:
      \label{ch:settheory}    <a name="ch:settheory"></a> 
      \ref{ch:settheory}      <a href="#ch:settheory">the_chapter_number</a> 
      \label{eq:euler} to <a name="eq:euler"></a> 
      \ref{eq:euler}   to <a href="#eq:euler">the_equation_number</a> 

    The label should be appended to the object representing the surrounding object 
    The object's numeric label is set automatically
    These are combined in a (user_label, numeric_label) lookup table
    example
      latex:  \begin{formative}\label{fo:settheory} ... \end{formative}
      xml:    <formative label="fo:settheory"> ... </formative>
      xhtml:  <div class="formative" label="fo:settheory"> .. </div>
      object: Exercise(type="formative", label="fo:settheory)


    #--------------------
    Mandatory database fields
    #--------------------
    parent      parent
    node_id     serial number
    node_class  division, theorem, list, ...
    node_type   chapter, lemma, itemize, ...

    #--------------------
    Django templates
    #--------------------
    division: (chapter|section|subsection)
    translate to <h1 class="chapter"> ... </h1>

    list: (itemize|enumerate|questions|parts|subparts)
    translate to <ul class="itemize"> ... </ul> etc.

    item: (item|question|part|subpart|choice|correctchoice|step)
    translate to <li class="question"> ... </li>

    float: (table|figure)
    translate to <img src="filename" number="1.3" caption="Onions" label="fig:onions" /> 
    translate to <div class="table" number="1.5" caption="Results" label="tab:results"> ... </div> 

    tabular: (tabular|tabbing)
    translate to <table> ... </table>    

    exercise: (diagnostic|formative|summative)
    translate to <div class="diagnostic" number="2.2" label="di:setheory"> ... </div>

    theorem: (definition|proposition|lemma|theorem|corollary)
    translate to <div class="lemma" number="3.1" caption="Zorn's Lemma" label="lem:zorn"> ... </div>

    box: (proof|answer|hint)
    translate to <div class="proof"> ... </div>


'''


#------------------------------------------------
# imports
import sys, os, re, logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

import camel.models

#------------------------------------------------
# globals
out = logging.getLogger(__name__)
labels = dict()

#------------------------------------------------
# classes
#------------------------------------------------
# Node: basic document tree node
class Node(object):
    counter = 0    
    def __init__(self):
        Node.counter += 1
        self.node_id = Node.counter
        self.children = []
        self.parent = None
        
    #-----------------------------
    # mpath output
    def mpath(self):
        if not self.parent:
            return '00'
        idx = self.parent.children.index(self)
        hxstr = hex( idx )[2:].zfill(2)
        return self.parent.mpath() + '.' + hxstr

    #-----------------------------
    # recursive text output
    def __repr__(self, level=0):
        # s = '----'*level
        s = self.mpath() + ': '
        # if self.parent:
        #     s += '<parent: ' + self.parent.__class__.__name__ + '[' + str(self.parent.node_id) + ']> '
        s += self.__class__.__name__ 
        # s += ' [' + str(self.node_id) + ']'
        if hasattr(self, 'number'):
            s += ': ' + str( self.number[-1] )
        if hasattr(self, 'title'):
            s += ': ' + self.title
        if hasattr(self, 'htex'):
            s += ': ' + self.htex
        if hasattr(self, 'target'):
            s += ': ' + self.target
        s += '\n'
        for child in self.children:
            s += child.__repr__(level+1)
        return s
    
    #-----------------------------
    # recursive xml output
    def xml(self):
        # create element
        element = ET.Element(self.__class__.__name__)
        # set attributes
        element.set('node_id', str(self.node_id))
        if hasattr(self, 'number'):
            element.set('number',  '.'.join([str(c) for c in self.number]))
        if hasattr(self, 'title'):
            element.set('title', self.title)
        if hasattr(self, 'label') and self.label:
            element.set('label', self.label)
        if hasattr(self, 'htex'):
            element.text = self.htex.strip()
        # recursive call
        for child in self.children:
            child_element = child.xml()
            element.append(child_element)
        return element

    #-----------------------------
    # recursive camel database output
    def camel_tree(self, module, parent=None, commit=False, is_readonly=False):

        # create treenode
        t = camel.models.TreeNode(node_id=self.node_id, mpath=self.mpath)

        # set attributes
        t.module = module
        if parent:
            t.parent = parent
        t.is_readonly = is_readonly            
        t.node_type = self.__class__.__name__.lower()
        t.node_class = node_class[t.node_type]
        t.mpath = module.code + '.' + self.mpath()
        if hasattr(self, 'label'):
            t.label = self.label
        if hasattr(self, 'number'):
            t.number = self.number[-1]
        if hasattr(self, 'title'):
            t.title = self.title
        if hasattr(self, 'htex'):
            t.htex = self.htex
        if hasattr(self, 'is_correct_choice'):
            t.is_correct_choice = self.is_correct_choice
                  
        # write to database (note: nodes not inserted in sequential order)
        print t
        if commit: 
            t.save()

        # recursive call
        for child in self.children:
            child.camel_tree(module, parent=t, commit=commit)
        
#-----------------------------
# Block: Node with a title and/or label (both can be null)
class Block(Node):
    def __init__(self, title=None, label=None):
        Node.__init__(self)
        if title:
            self.title = title
        if label:
            self.label = label

#-----------------------
# Division (abstract)
# set and reset counters here
class Division(Block):
    def __init__(self, title=None, label=None):
        Block.__init__(self, title, label)

class Chapter(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Chapter.counter += 1
        self.number = [Chapter.counter]
        Section.counter = 0
        Subsection.counter = 0
        Theorem.counter = 0
        Figure.counter = 0
        Table.counter = 0
        List.counter = 0
    
class Section(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Section.counter += 1
        self.number = [Chapter.counter, Section.counter]
        Subsection.counter = 0

class Subsection(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Subsection.counter += 1
        self.number = [Chapter.counter, Section.counter, Subsection.counter]
    
#-----------------------------
# Theorems
# single counter, reset by Chapter
#-----------------------------
class Theorem(Block):
    counter = 0
    def __init__(self, title=None, label=None):
        Block.__init__(self, title, label)
        Theorem.counter += 1
        self.number = [Chapter.counter, Theorem.counter]

class Lemma(Theorem):
    def __init__(self, title=None, label=None):
        Theorem.__init__(self, title, label)

class Corollary(Theorem):
    def __init__(self, title=None, label=None):
        Theorem.__init__(self, title, label)

class Definition(Theorem):
    def __init__(self, title=None, label=None):
        Theorem.__init__(self, title, label)

class Remark(Theorem):
    def __init__(self, title=None, label=None):
        Theorem.__init__(self, title, label)

class Example(Theorem):
    def __init__(self, title=None, label=None):
        Theorem.__init__(self, title, label)
#-----------------------------
# Exercise
# single counter, reset by Chapter
#-----------------------------
class Exercise(Block):
    counter = 0
    def __init__(self, title=None, label=None):
        Block.__init__(self, title, label)
        Exercise.counter += 1
        self.number = [Chapter.counter, Exercise.counter]
        Question.counter = 0
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

class Diagnostic(Exercise):
    def __init__(self, title=None, label=None):
        Exercise.__init__(self, title, label)

class Formative(Exercise):
    def __init__(self, title=None, label=None):
        Exercise.__init__(self, title, label)

class Summative(Exercise):
    def __init__(self, title=None, label=None):
        Exercise.__init__(self, title, label)

#-----------------------------
# Lists 
# when mpaths properly implemented, we can probably get rid of the List counter
#-----------------------------
class List(Node):
    counter = 0
    def __init__(self):
        Node.__init__(self)
        List.counter += 1
        self.number = [Chapter.counter, List.counter]
        Item.counter = 0

class Itemize(List):
    def __init__(self):
        List.__init__(self)

class Enumerate(List):
    def __init__(self):
        List.__init__(self)

class Questions(List):
    def __init__(self):
        List.__init__(self)

class Parts(List):
    def __init__(self):
        List.__init__(self)

class Subparts(List):
    def __init__(self):
        List.__init__(self)

class Choices(List):
    def __init__(self):
        List.__init__(self)

class Steps(List):
    def __init__(self):
        List.__init__(self)

#-----------------------------
# Item (item number is passed to the constructor)
#-----------------------------
class Item(Node):
    counter = 0
    def __init__(self, item_number):
        Node.__init__(self)
        Item.counter += 1
        self.number = item_number

class Question(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Question.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter]
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

class Part(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Part.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter]
        Subpart.counter = 0
        Choice.counter = 0

class Subpart(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Subpart.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter, Subpart.counter]
        Choice.counter = 0

class Choice(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Choice.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter, Subpart.counter, Choice.counter]
        self.correctchoice = False

class Step(Item):
    def __init__(self, item_number):
        Item.__init__(self, item_number)


#-----------------------------
# Boxes 
# Proof box should be "attached" to a Theorem object (using mpaths)
# Answer box should be "attached" to a Question/Part/Subpart object
#-----------------------------
class Box(Block):
    def __init__(self, title=None, label=None):
        Block.__init__(self, title, label)

class Proof(Box):
    def __init__(self, title=None, label=None):
        Box.__init__(self)

class Answer(Box):
    def __init__(self, title=None, label=None):
        Box.__init__(self)

class Solution(Box):
    def __init__(self, title=None, label=None):
        Box.__init__(self)

class Hint(Box):
    def __init__(self, title=None, label=None):
        Box.__init__(self)
class Center(Box):
    def __init__(self, title=None, label=None):
        Box.__init__(self)

#-----------------------------
# Floats
#-----------------------------
class Figure(Block):
    counter = 0
    def __init__(self, title=None, label=None, src=None):
        Block.__init__(self, title, label)
        Figure.counter += 1
        self.number = [Chapter.counter, Figure.counter]
        if src:
            self.src = src

class Table(Block):
    counter = 0
    def __init__(self, title=None, label=None):
        Block.__init__(self, title, label)
        Table.counter += 1
        self.number = [Chapter.counter, Table.counter]

class Tabular(Block):
    def __init__(self, title=None, label=None, htex=None):
        Block.__init__(self)
        if htex:
            self.htex = htex

#-----------------------------
# TexNode: here we perform partial latex to html translation
#   1. convert latex style commands to html (e.g textbf, textit)
#   2. scan for labels, references and citations
#   3. kill spurious latex commands (\maketitle, \tableofcontents, etc)
#-----------------------------
class Reference(Node):
    def __init__(self, htex=None):
        Node.__init__(self)
        self.htex = htex

class TexNode(Node):

    def __init__(self, s = None):
        Node.__init__(self)
        
        # check for all whitespace (in which case set content to empty string)
        # we test for empty tex nodes later, and delete them.
        if not s or not re.compile(r'\S+',re.DOTALL).search(s):
            self.htex = ''
            return
        
        # remove comments (line-by-line)
        lines = s.strip().split('\n')
        for idx in range( len(lines) ):
            lines[idx] = re.sub(r'\%.*$', "", lines[idx])
        s = '\n'.join(lines) + '\n'
        
        # parse \ref and \citation

        # labels and citations (need to use materialized paths here)
        # there should only be at most one label per tex block
        # labels should refer to the enclosing environment
        # pattern = re.compile(r'\\label\{([^\}]*)\}')
        # matches = re.finditer(pattern, s)
        # for match in matches:
        #         labels[ match.groups()[0] ] = self.mpath()

        # labels, references and citations
        # kill label commands (picked up in parse_block )
        s = re.sub(r'\\label\{([^\}]*)\}', r'',s)
        # s = re.sub(r'\\ref\{([^\}]*)\}', r'<a href="#\1">\1</a>',s)
        s = re.sub(r'\\cite\{([^\}]*)\}', r'<a href="bib:\1">here</a>',s)

        # font styles
        s = re.sub(r'\\emph\{([^\}]*)\}',r'<i>\1</i>',s)
        s = re.sub(r'\\textit\{([^\}]*)\}',     r'<i>\1</i>',s)
        s = re.sub(r'\\textbf\{([^\}]*)\}',     r'<b>\1</b>',s)
        s = re.sub(r'\\texttt\{([^\}]*)\}',     r'<tt>\1</tt>',s)
        s = re.sub(r'\\underline\{([^\}]*)\}',  r'<u>\1</u>',s)
        
        # spacing
        s = re.sub(r'\\vspace[\*]?\{[^\}]\w+\}',r'<p>',s)
        s = re.sub(r'\\hspace[\*]?\{[^\}]\w+\}',r'&nbsp;&nbsp;',s)
        
        # custom
        s = re.sub(r'\\proofomitted',           r'<i>[Proof omitted]</i><br/>', s)

        # layout
        s = re.sub(r'\\paragraph\{([^\}]*)\}',  r'<br>\n<b>\\1</b>\n',s)
        s = re.sub(r'\\par\s+',                 r'<br>',s)
        s = re.sub(r'\\bigskip\s+',             r'<br>',s)

        # tricky
        s = re.sub(r'\\percent', r'&#37;',s)
        s = re.sub(r'~', r' ',s)
        
        # kill
        s = re.sub(r'\\maketitle',      r'',s)
        s = re.sub(r'\\tableofcontents',r'',s)
        s = re.sub(r'\\clearpage',      r'',s)
        s = re.sub(r'\\break',          r'',s)
        s = re.sub(r'\\newpage',        r'',s)
        s = re.sub(r'\\label\{.*\}',    r'',s)
        s = re.sub(r'\\begin{center}',  r'',s)
        s = re.sub(r'\\end{center}',    r'',s)
        s = re.sub(r'\\centering',      r'',s)
        s = re.sub(r'\\hfill',          r'',s)
        s = re.sub(r'\\if.*',           r'',s)
        s = re.sub(r'\\small',          r'',s)
        s = re.sub(r'\\normalsize',     r'',s)
        s = re.sub(r'\\endinput',       r'',s)
        s = re.sub(r'\\makefrontmatter',r'',s)
        s = re.sub(r'\ ',               r' ',s)
            
        # tidy up
        self.htex = s.strip()
    

#-----------------------------
# Book class (root node of document tree)
class Book(Node):
    # init
    def __init__(self):
        Node.__init__(self)
        Chapter.number = 0
        Section.counter = 0
        Subsection.counter = 0
        Theorem.counter = 0
        Figure.counter = 0
        Table.counter = 0
        List.counter = 0

    # prettyprint xml tree
    def prettyprint_xml(self):
        xml_tree = self.xml()
        xml_str = ET.tostring(xml_tree, 'utf-8')
        dom = minidom.parseString(xml_str)
        pi = dom.createProcessingInstruction('xml-stylesheet', 'type="text/css" href="cameltex.css"')
        root = dom.firstChild
        dom.insertBefore(pi, root)
        return dom.toprettyxml(indent="  ")


#-----------------------------
# correspondence between latex cmds/envs to doctree classes
# usage: doctree_class[node_class][node_type]
doctree_class = {
    'division': {
        'book':         Book,
        'chapter':      Chapter,
        'section':      Section,
        'subsection':   Subsection,
    },    
    'list':     {
        'itemize':      Itemize,
        'enumerate':    Enumerate,
        'questions':    Questions,
        'parts':        Parts,
        'subparts':     Subparts,
        'choices':      Choices,
        'steps':        Steps,
    },
    'item':     {
        'item':         Item,
        'question':     Question,
        'part':         Part,
        'subpart':      Subpart,
        'choice':       Choice,
        'step':         Step,
    },
    'exercise': {
        'exercise':     Exercise,
        'diagnostic':   Diagnostic,
        'formative':    Formative,
        'summative':    Summative,
    },
    'float': {
        'figure':       Figure,
        'table':        Table,
        'tabular':      Tabular,
    },
    'theorem':  {
        'theorem':      Theorem,
        'definition':   Definition,
        'lemma':        Lemma,
        'corollary':    Corollary,
        'remark':       Remark,
        'example':      Example,
    },
    'box': {
        'proof':        Proof,
        'answer':       Answer,
        'solution':     Solution,
        'hint':         Hint,
        'center':         Center,
    },
    'ignored': {
        'equation':     None,
        'cases':        None,
        'align':        None,
        'array':        None,
    },
    'content': {
        'texnode':      TexNode,
        'reference':    Reference,
    },
}

# item dictionary
item_dict = {
    'itemize':      'item',
    'enumerate':    'item',
    'questions':    'question',
    'parts':        'part',
    'subparts':     'subpart',
    'choices':      'choice',
    'steps':        'step',
}

# node_type grouped by node_class
node_types = { key : tuple( doctree_class[key].keys() ) for key in doctree_class.keys() }
    
# node_class grouped by node_type
node_class = dict([ (k2,k1) for k1 in doctree_class.keys() for k2 in doctree_class[k1].keys() ])


#-----------------------------
# TexParser class (root node of document tree)
class TexParser(object):
    # init
    def __init__(self):
        pass

    
    # read latex (recursive)
    def read_latex(self, filename, level=0):
        if level > 4:
            print('error: read_body: recursion limit reached (max = 4)')
            return ''
        
        # open file
        with open(filename) as f:
            f_str = f.read()
        
            # remove comments (line-by-line)
            lines = f_str.strip().split('\n')
            for idx in range( len(lines) ):
                lines[idx] = re.sub(r'\%.*$', "", lines[idx])
            f_str = '\n'.join(lines) + '\n'
        
            # find input commands
            pattern = re.compile(r'[^%+]\\input\{([^\}]*)\}')
            matches = re.finditer(pattern, f_str)
            
            # return contents if no \input commands (end recursion)
            if not matches:
                return f_str
            
            # otherwise process \input commands
            else:
                s = ''
                sIdx = 0
                for match in matches:
                    eIdx = match.start()
                    s += f_str[ sIdx:eIdx ]
                    sIdx = match.end()
                    nested_filename = match.groups()[0]
                    # append .tex extension if necessary
                    if not re.search(r'\.', nested_filename):
                        nested_filename = nested_filename + '.tex'
                    nested_filename = os.path.join(os.path.dirname(filename), nested_filename)
                    out.info('File: %s', nested_filename)
                    # recursive call
                    s += self.read_latex(nested_filename, level=level+1)
                s += f_str[sIdx:]
                return s
    
    
    # read preamble (shallow)
    def read_preamble(self, filename):
        with open(filename) as f:
            f_str = f.read()
            pattern = r'(.*)\\begin\{document\}' 
            match = re.compile(pattern, re.DOTALL).search( f_str )
            preamble = match.groups()[0] if match else ''
            return preamble

    # read body (recursive)
    def read_body(self, filename):
        s = self.read_latex(filename)
        s = self.fix_latex(s)
        pattern = r'\\begin{document}(.*)\\end{document}' 
        match = re.compile(pattern, re.DOTALL).search( s )
        body = match.groups()[0] if match else ''
        return body

    # fix naughty macros
    def fix_latex(self, s):
        s = re.sub(r'\\bit\s+', r'\\begin{itemize} ', s)
        s = re.sub(r'\\eit\s+', r'\\end{itemize} ', s)
        s = re.sub(r'\\ben\s+', r'\\begin{enumerate} ', s)
        s = re.sub(r'\\een\s+', r'\\end{enumerate} ', s)
        s = re.sub(r'\\it\s+', r'\\item ', s)
        return s
        
    
    # parse main.tex
    def parse_main(self, main_file):

        # check preamble
        if not self.check_preamble( main_file ):
            out.error('Errors in main.tex - aborting.')
            print('Errors in main.tex - aborting.')
            return None

        preamble_data = self.parse_preamble( main_file )
        book = self.parse_body( main_file )
        book.title = preamble_data['book_title']
        return book

    # check preamble
    def check_preamble(self, main_file):
        '''
        check that mandatory fields are set
        '''
        preamble = self.read_preamble( main_file )
    
        # document class (should be "camel" with no options) 
        pattern = r'\\documentclass(\[.*\])?\{([^\}]+)\}'
        match = re.compile(pattern).search( preamble )
        if not match or not match.groups()[1] == 'camel':
            out.error('document class must be "camel"')
            print('document class must be "camel"')
            return False

        # module code
        match = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
        if not match:
            out.error(r'\modulecode{} missing in preamble')
            print(r'\modulecode{} missing in preamble')
            return False

        # academic year
        match = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
        if not match:
            out.error(r'\academicyear{} missing in preamble')
            print(r'\academicyear{} missing in preamble')
            return False
            
        # ok
        return True
    
    
    # parse preamble 
    def parse_preamble(self, main_file):    

        preamble  = self.read_preamble( main_file )
        preamble_data = {
            'module_code':      None,
            'academic_year':    None,
            'module_title':     None,
            'book_title':       None,
            'new_commands':     '',
        }
        match = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
        if match: 
            preamble_data['module_code'] = match.groups()[0]
        match = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
        if match: 
            preamble_data['academic_year'] = match.groups()[0]
        match = re.compile(r'\\moduletitle\{(.*)\}').search( preamble )
        if match: 
            preamble_data['module_title'] = match.groups()[0]
        match = re.compile(r'\\booktitle\{(.*)\}').search( preamble )
        if match:
            preamble_data['book_title'] = match.groups()[0]
        # new commands (keep as latex for mathjax to handle)
        newcmds = []
        pattern = re.compile(r'(\\newcommand\{(\w+)\}\{.*\})') # dodgy
        matches = re.finditer(pattern, preamble)
        for match in matches:
            newcmds.append( match.groups()[0] )
        preamble_data['new_commands'] = '\n'.join( newcmds )
    
        return preamble_data

    
    # parse body 
    def parse_body(self, main_file):
        '''
        chop into chapters/sections/subsections
        call parse_block recursively on the resulting blocks
        '''
        body = self.read_body( main_file )
        book = Book()

        # find all division commands 
        pattern = r'\\(chapter|section|subsection)\{([^\}]*)\}'
        matches = re.finditer(pattern, body)

        # init stack
        stack = [ book ]
        start_block = 0
        
        # iterate over division commands
        for match in matches: 
            node_type   = match.groups()[0]
            node_title  = match.groups()[1]
            end_block   = match.start()             # end index of block before current division command
            tex_str     = body[ start_block : end_block ]

            # Call parse_block on tex_str
            # This tex_str is the block located BEFORE the current division command
            # The tex_str located AFTER the very last division is processed separately at the end
            children = self.parse_block( tex_str, parent=stack[-1] )
            # for child in children:
            #     child.parent = stack[-1]
            stack[-1].children.extend( children )
            # stack[-1].label = label

            # chapter/section/subsection: close current subsection (if any) and append it to enclosing section
            if node_type in ['chapter', 'section', 'subsection']:
                if type(stack[-1]) == Subsection:
                    ss = stack.pop()
                    stack[-1].children.append( ss )
                # chapter/section: close current section (if any) and append it to enclosing chapter
                if node_type in ['section', 'chapter']:
                    if type(stack[-1]) == Section:
                        se = stack.pop()
                        stack[-1].children.append( se )
                    # chapter: close current chapter (if any) and append it to document root
                    if node_type == 'chapter':
                        if type(stack[-1]) == Chapter:
                            ch = stack.pop()
                            stack[-1].children.append( ch )
                        # push new chapter onto stack
                        ch = Chapter( node_title )
                        print '++++++++++++++++++++++++' + ch.title
                        ch.parent = stack[-1]
                        stack.append( ch )
                    # push new section onto stack
                    else:
                        se = Section( node_title )
                        se.parent = stack[-1]
                        stack.append( se )
                # push new subsection onto stack
                else: 
                    ss = Subsection( node_title )
                    ss.parent = stack[-1]
                    stack.append( ss )

            # update start_idx for next match
            start_block = match.end()

        # clean up tail (after last match has been processed)
        # last division command could be chapter, section or subsection
        tex_str = body[ start_block : len(body) ]
        print tex_str
        children = self.parse_block( tex_str, parent=stack[-1] )
        # for child in children:
        #     child.parent = stack[-1]
        last_division = stack.pop()
        last_division.children.extend( children )
        # last_division.label = label
        stack[-1].children.append( last_division )    # append last division to parent

        # pop off enclosing environments until we reach the root
        while len(stack) > 1:
            node = stack.pop()
            stack[-1].children.append( node )

        # return the root node (book)
        return stack.pop()
    
    # chop into alternating tex and env blocks
    def find_blocks(self, tex_str):
        '''
        returns list of [node_type, node_title, start_idx, end_idx] 
            0: node_type
            1: node_title
            2: start_idx
            3: end_idx
        '''
        # initialise arrays
        stack = []
        blocks = []
        
        # append first slice: always a tex block (empty blocks are removed later)
        # initially it contains the entire tex string
        # second index will be overwritten unless "tex_str" contains only one block
        # the final entry is the block title
        blocks.append([ 'tex', '', 0, len(tex_str) ])

        # find all environment delimiters (catches theorem/exercise names or tabular column format string)
        pattern = r'\\(begin|end)\{(\w+)\}(\[(.*)\]|\{(.*)\})*'
        matches = re.finditer(pattern, tex_str)

        # old school
        timeout=False
        ignored_type = None
        
        # loop over environment delimiters
        for match in matches: 
            
            # current match
            groups = match.groups()
            
            bore        = groups[0]
            node_type   = groups[1]
            node_title  = groups[3] if groups[3] else ''
            
            # check if "begin"
            if groups[0] == 'begin':

                # print ">>> BEGIN %s, timeout = %s" % (groups[1], timeout)
                
                # start timeout if beginning of an ignored environment
                # save name of ignored type so that we can stop timeout
                # when the corresponding \end is encountered.
                if node_type in node_types['ignored']:
                    ignored_type = node_type
                    timeout=True
                
                if not timeout:
                    # push environment name onto stack
                    stack.append( node_type )
                    # extend slices only if level-one environment
                    if len(stack) == 1:
                        # set end_idx of preceeding block
                        blocks[-1][3] = match.start()
                        # append new block for current environment (contains remainder of tex_str)
                        blocks.append([ node_type, node_title, match.end(), len(tex_str) ])
                        

            # otherwise it's "end"
            else:

                # print ">>> END %s, timeout = %s" % (groups[1], timeout)

                if not timeout:
                    # pop name off stack (and check that it co-incides with current node_type )
                    assert node_type == stack.pop()
                    # extend blocks only if it's the end of level-one environment
                    if len(stack) == 0:
                        # set end_idx of previous block
                        blocks[-1][3] = match.start()
                        # append new 'tex' block (to cap off this environment)
                        blocks.append([ 'tex', '', match.end(), len(tex_str) ])
                else:
                    # end timeout if necessary
                    if groups[1] == ignored_type:
                        timeout = False

        # end iterate over matches
        return blocks

    
    # parse_block (returns children and label)
    def parse_block(self, tex_str, parent=None):

        # find sub-blocks
        blocks = self.find_blocks(tex_str)

        # search tex sub-blocks for label 
        def find_label(blocks):
            pattern = r'\\label\{([^\}]*)\}'
            for block in blocks:
                if block[0] == 'tex':
                    match = re.search(pattern, tex_str[ block[2]:block[3] ])
                    if match:
                        return match.groups()[0]
            return None

        # if label found, attach to parent
        label = find_label(blocks)
        if parent and label:
            parent.label = label
        
        # process sub-blocks and create tree nodes (recursive calls here)
        children = []

        # iterate through sub-blocks
        for block in blocks:

            # init local variables (descriptive names)
            block_name = block[0]
            block_title = block[1]
            start_index = block[2]
            end_index = block[3]
            content = tex_str[ start_index:end_index  ]
                        
            # lists (handled by parse_list_contents)
            if block_name in node_types['list']:
                classname = doctree_class['list'][block_name]
                node = classname()
                item_name = item_dict[block_name] # string
                node.children = self.parse_list_contents(content, parent=node, item_name=item_name)
            
            # theorems
            elif block_name in node_types['theorem']:
                classname = doctree_class['theorem'][block_name]
                node = classname()
                if block_title:
                    node.title = block_title
                node.children = self.parse_block( content, parent=node )
            
            # exercises
            elif block_name in node_types['exercise']:
                classname = doctree_class['exercise'][block_name]
                node = classname()
                if block_title:
                    node.title = block_title
                node.children = self.parse_block( content, parent=node )
            
            # boxes
            elif block_name in node_types['box']:
                classname = doctree_class['box'][block_name]
                node = classname()
                node.children = self.parse_block( content, parent=node )
            
            # floats
            elif block_name in node_types['float']:
                classname = doctree_class['float'][block_name]
                node = classname()
                
                # table 
                if block_name == 'table':
                    match = re.compile(r'\\caption\{([^\}]+)\}').search(content)
                    if match:
                        node.title = match.groups()[0]
                        content = content[:match.start()] + content[match.end():]
                    node.children = self.parse_block( content, parent=node )

                # figures
                elif block_name == 'figure':
                    match = re.compile(r'\\caption\{([^\}]+)\}').search(content)
                    if match:
                        node.title = match.groups()[0] 
                    match = re.compile(r'\\includegraphics(\[[^\]]*\])\{([^\}]+)\}').search(content)
                    if match:
                        node.src = match.groups()[1] 

                # tabular
                elif block_name == 'tabular':
                    s = ''
                    content = re.sub(r'\\hline','', content)
                    # print content
                    rows = content.split(r'\\')
                    for row in rows:
                        if not row or not re.compile(r'\S+',re.DOTALL).search(row):
                            break
                        s += '<tr>'
                        cells = row.split(r'&')
                        for cell in cells:
                            s += '<td>' + cell + '</td>'
                        s += '</tr>'
                    # if content = re.sub(r'\s&','</td><td>', content)
                    # content = re.sub(r'^&|\s&','</td><td>', content)
                    # content = re.sub(r'\\\\','</td></tr>', content)
                    node.htex = s
                                    
            # default is texnode
            else:
                node = TexNode( content )

            # add node to children (with hack to eliminate empty tex nodes)
            node.parent = parent
            if not type(node) == TexNode:
                children.append( node )
            elif node.htex:
                pattern = r'\\ref\{([^\}]+)\}'
                matches = re.finditer(pattern, node.htex)
                if not matches:
                    children.append( node )
                else:
                    start_idx = 0;
                    for match in matches: 
                        end_idx = match.start()
                        node = TexNode( node.htex[ start_idx: end_idx ] )
                        node.parent = parent
                        children.append( node )
                        node = Reference( match.groups()[0] ) 
                        node.parent = parent
                        children.append( node )
                        start_idx = match.end()
                    node = TexNode( node.htex[ start_idx: ] )
                    node.parent = parent
                    children.append( node )
            
        return children




    # parse list contents
    def parse_list_contents(self, tex_str, parent, item_name="item"):
        '''
        Returns a list of item nodes. These become the only children of the enclosing list node
        The number of enclosing list is passed so that item numbers can be set properly    
        '''
       # find class correpsonding to this type of item
        if item_name in node_types['item']:
            item_class = doctree_class['item'][item_name]
        else:
            return []

        # function to skip over environments to find the next item
        def find_next_item(tex_str, item_name='item'):
            
            # hack for correctchoice (multiplie choice questions)
            if item_name == 'choice':
                item_name = 'choice|correctchoice'
            
            # find all item tokens and environment delimiters
            pattern = r'\\(' + item_name + r')|\\(begin|end)\{(\w+)\}' 
            matches = re.finditer(pattern, tex_str)
            
            # return entire tex_str if no matches at all 
            if not matches:
                return tex_str, []

            # get first match and make sure that it really is an item
            first_match = matches.next()
            if not first_match.groups()[0]:
                return tex_str, []

            # hack to catch correctchoice (multiple choice questions)
            correct_choice = False
            if first_match.groups()[0] == 'correctchoice':
                correct_choice = True

            # use stack to keep track of levels
            start_idx = first_match.end()
            stack = []
            for match in matches:
                groups = match.groups()
                if groups[1]:
                    if groups[1] == 'begin':
                        stack.append( groups[2] )
                    else:
                        stack.pop()
                else:
                    # return to calling environment when stack empty (next item reached)
                    if len(stack) == 0:
                        end_idx = match.start()
                        # return (block_content, tail_content, correct_choice_flag)
                        return tex_str[start_idx:end_idx], tex_str[ end_idx:len(tex_str) ], correct_choice

            # return final item content
            # format (block_content, empty_tail, correct_choice_flag)
            return tex_str[ start_idx:len(tex_str) ], '', correct_choice



        # initialise list to hold items
        item_list = []
        item_counter = 1
        
        # chop it up (recursive calls to parse_block here)
        # item numbers are processed in the calling environment
        # and passed to each item on creation.
        tail = tex_str
        while tail:
            block, tail, correct_choice = find_next_item(tail, item_name=item_name)
            item_number = list( parent.number ) # copy
            item_number.append(item_counter)
            item_counter += 1
            item = item_class(item_number)
            item.parent = parent
            if type(item) == Choice and correct_choice:
                item.is_correct_choice = True
            item.children = self.parse_block( block, parent=item )
            item_list.append( item )

        return item_list


#------------------------------------------------
# main
#------------------------------------------------
def main(args=None):
    
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [-v] [-q] [-x] [latex_main]", version="%prog: version 0.1", add_help_option=True)
    parser.add_option("-v", "--verbose", action="store_false", dest="verbose", help="verbose output")
    parser.add_option("-x", "--xml", action="store_true", dest="xml", help="print xml tree to stdout")
    parser.add_option("-t", "--text", action="store_true", dest="text", help="print text tree to stdout")
    parser.add_option("-d", "--camel", action="store_true", dest="camel", help="update camel database (dry run)")
    parser.add_option("-c", "--commit", action="store_true", dest="commit", help="update camel database (commit changes)")
    parser.set_defaults(verbose=True, demo=False, text=False, xml=False, camel=False, commit=False)

    (options, args) = parser.parse_args()
    if not args:
        print 'usage: $python doctree.py main.tex (camel.cls)'
        return

    # test new stuff
    main_tex = args[0]
    p = TexParser()
    preamble = p.parse_preamble( args[0] )
    book = p.parse_main( main_tex )
    book.title = preamble['book_title']

    # text output
    if options.text:
        print book

    # xml output
    if options.xml:
        print book.prettyprint_xml()

    # camel database output
    if options.camel:
        
        # hack to set user-defined latex macros
        nc = ''
        nc += r'\newcommand{\N}{\mathbb{N}}'
        nc += r'\newcommand{\Z}{\mathbb{Z}}'
        nc += r'\newcommand{\R}{\mathbb{R}}'
        nc += r'\newcommand{\C}{\mathbb{C}}'
        nc += r'\newcommand{\prob}{\mathbb{P}}'
        nc += r'\newcommand{\expe}{\mathbb{E}}'
        nc += r'\newcommand{\var}{\text{Var}}'
        nc += r'\newcommand{\cov}{\text{Cov}}'
        nc += r'\newcommand{\supp}{\text{supp}}'

        # check whether this module already exists in the database
        code = preamble['module_code']
        year = preamble['academic_year']
        modules = camel.models.Module.objects.filter(code=code, year=year)
        if not modules:
            out.info( 'Creating new module %s/%s' % (code, year) )
            mo = camel.models.Module(code=code, year=year, title=preamble['module_title'])
            mo.save()
        elif len(modules) == 1:
            out.info( 'Updating existing module %s/%s (existing doctree will be deleted)' % (code, year) )
            mo = modules[0]
            for bo in camel.models.TreeNode.objects.filter(module=mo):
                bo.delete()
        else:
            out.error('The database contains more than one module with code %s and year %s ... SORT IT OUT!' % (code, year) )
            return

        # set module newcommands (hack)
        mo.newcommands = nc
        mo.save()

        # write to database
        if options['commit']:
            book.camel_tree(module=mo, commit=True)
        else:
            book.camel_tree(module=mo, commit=False)
          
if __name__ == '__main__':
    main()

