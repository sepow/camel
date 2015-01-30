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
debug = True
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
        self.mpath = ''
        self.children = []
        
    #-----------------------------
    # recursive text output
    def __repr__(self, level=0):
        s = '----'*level + self.__class__.__name__ + ' [' + str(self.node_id) + ']'
        if hasattr(self, 'number'):
            s += ': ' + str( self.number[-1] )
        if hasattr(self, 'title'):
            s += ': ' + self.title
        if hasattr(self, 'htex'):
            s += '>>>>> ' + self.htex + ' <<<<<'
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
    def __init__(self, title=None, label=None, htex=None):
        Block.__init__(self)
        Table.counter += 1
        self.number = [Chapter.counter, Table.counter]
        if htex:
            self.htex = htex

#-----------------------------
# Content 
# TexNode: partial latex to html translation
# Here we process the following types of latex command
#   1. convert latex style commands to html (e.g textbf, textit)
#   2. process labels, references and citations
#   3. kill spurious latex commands (\maketitle, \tableofcontents, etc)
#-----------------------------
class TexNode(Node):

    def __init__(self, s = None):
        Node.__init__(self)
        
        # check for all whitespace (in which case set content to empty string)
        if not s or not re.compile(r'\S+',re.DOTALL).search(s):
            self.htex = ''
            return
        
        # remove comments (line-by-line)
        lines = s.strip().split('\n')
        for idx in range( len(lines) ):
            lines[idx] = re.sub(r'\%.*$', "", lines[idx])
        s = '\n'.join(lines) + '\n'

        # labels and citations (need to use materialized paths here)
        pattern = re.compile(r'\\label\{([^\}]*)\}')
        matches = re.finditer(pattern, s)
        for match in matches:
                labels[ match.groups()[0] ] = self.mpath

        # references and citations
        s = re.sub(r'\\ref\{([^\}]*)\}', r'<a href="\1">here</a>',s)
        s = re.sub(r'\\cite\{([^\}]*)\}', r'<a href="bib:\1">here</a>',s)

        # font styles
        s = re.sub(r'\\emph\{([^\}]*)\}',r'<i>\1</i>',s)
        s = re.sub(r'\\textit\{([^\}]*)\}',     r'<i>\1</i>',s)
        s = re.sub(r'\\textbf\{([^\}]*)\}',     r'<b>\1</b>',s)
        s = re.sub(r'\\underline\{([^\}]*)\}',  r'<u>\1</u>',s)
        
        # spacing
        s = re.sub(r'\\vspace[\*]?\{[^\}]\w+\}',r'<p>',s)
        s = re.sub(r'\\hspace[\*]?\{[^\}]\w+\}',r'&nbsp;&nbsp;',s)
        
        # custom
        s = re.sub(r'\\proofomitted',           r'<i>[Proof omitted]</i><br/>', s)

        # layout
        s = re.sub(r'\\paragraph\{([^\}]*)\}',  r'<br>\n<b>\\1</b>\n',s)
        s = re.sub(r'\\par\s+',                    r'<br>',s)

        # tricky
        s = re.sub(r'\\percent', r'&#37;',s)
        
        # kill
        s = re.sub(r'\\maketitle',      r'',s)
        s = re.sub(r'\\tableofcontents',r'',s)
        s = re.sub(r'\\clearpage',      r'',s)
        s = re.sub(r'\\break',          r'',s)
        s = re.sub(r'\\newpage',        r'',s)
        s = re.sub(r'\\hline',          r'',s)
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
            
        # tidy up
        self.htex = s.strip()
    
#------------------------------------------------
# correspondence between latex environments and camel classes
# must use the actual classes, rather than their names (str)
#------------------------------------------------

#-----------------------------
# Book class (root node of document tree)
class Book(Node):
    #-----------------------------
    # init
    def __init__(self, main_file=None):
        Node.__init__(self)
        if main_file:
            preamble = read_preamble( main_file )
            body = read_body( main_file )
            print preamble
            if preamble and body:
                self.parse_preamble(preamble)
                self.parse_body(body)

    #-----------------------------
    # parse preamble
    def parse_preamble(self, preamble):
    
        # check document class (should be "camel" with no options) 
        match = re.compile(r'\\documentclass\{([^\}]+)\}').search( preamble )
        if match and not match.groups()[0] == 'camel':
            print 'error: document class must be "camel"'
            return False

        # year
        year = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
        if match:
            self.year = match.groups()[0]

        # code
        code = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
        if match:
            self.code = match.groups()[0]

        # module title
        match = re.compile(r'\\moduletitle\{(.*)\}').search( preamble )
        if match:
            self.title = match.groups()[0]

        # book title
        match = re.compile(r'\\title\{(.*)\}').search( preamble )
        if match:
            self.booktitle = match.groups()[0]

        # extract new commands (keep as latex for mathjax to handle) 
        pattern = re.compile(r'(\\newcommand\{(\w+)\}\{.*\})') # dodgy
        matches = re.finditer(pattern, preamble)
        for match in matches:
            self.newcommands.append( TexNode( match.groups()[0] ) ) 
        
    
    #-----------------------------
    # parse body
    def parse_body(self, body):
        '''
        slices body into chapter/sections/subsections then
        parses each block, recursively splitting into alternate tex and environment blocks
        a tex block is one that contains no environments.
        recursive calls are to "parse_block" (below)
        '''

        # find all division commands
        pattern = r'\\(chapter|section|subsection)\{([^\}]*)\}'
        matches = re.finditer(pattern, body)

        # build tree
        start_idx= 0
        stack = []
        stack.append(self)
        for match in matches: 
            name    = match.groups()[0]
            title   = match.groups()[1]
            end_idx = match.start()
            tex_str = body[start_idx:end_idx]

            # This tex_str is the block located BEFORE the current division command
            # The tex_str located AFTER the very last division is processed separately at the end  
            stack[-1].children.extend( self.parse_block(tex_str) )

            # chapter/section/subsection: close current subsection (if any) and append it to enclosing section
            if name in ['chapter', 'section', 'subsection']:
                if type(stack[-1]) == Subsection:
                    subsec = stack.pop()
                    stack[-1].children.append(subsec)
                # chapter/section: close current section (if any) and append it to enclosing chapter
                if name in ['section', 'chapter']:
                    if type(stack[-1]) == Section:
                        sec = stack.pop()
                        stack[-1].children.append(sec)
                    # chapter: close current chapter (if any) and append it to document root
                    if name == 'chapter':
                        if type(stack[-1]) == Chapter:
                            chap = stack.pop()
                            stack[-1].children.append(chap)
                        # push new chapter onto stack
                        stack.append( Chapter(title) )
                    # push new section onto stack
                    else:
                        stack.append( Section(title) )
                # push new subsection onto stack
                else: 
                    stack.append( Subsection(title) )

            # update start_idx for next match
            start_idx = match.end()

        # clean up tail (after last match has been processed)
        tex_str = body[start_idx:len(body)]
        last_division = stack.pop()
        last_division.children.extend( self.parse_block(tex_str) )
        stack[-1].children.append( last_division )    # append last division to parent

        # pop off enclosing environments until we reach the root
        while len(stack) > 1:
            element = stack.pop()
            stack[-1].children.append(element)

        # check that the root is still "self"
        assert(self == stack.pop())

    #-----------------------------
    # parse_block 
    def parse_block(self, tex_str):
        #-----------------------------
        # Part 1: slice into alternate tex and environment blocks (these are sub-blocks of "self")
        #-----------------------------

        # initialise arrays
        blocks = []
        stack = []
        
        # append first block: always a tex block (empty blocks are removed later)
        # second index will be overwritten unless "self" contains only one block
        blocks.append([ 'tex', 0, len(tex_str)])

        # find all environment delimiters
        pattern = r'\\(begin|end)\{(\w+)\}'
        matches = re.finditer(pattern, tex_str)

        # loop over matches
        for match in matches: 
            
            # current match
            groups = match.groups()
            
            # check if "begin"
            if groups[0] == 'begin':
                # push name onto stack
                stack.append( groups[1] )
                # extend slices only if level-one environment
                if len(stack) == 1:
                    # set end_idx of previous block
                    blocks[-1][2] = match.start()
                    # append new block (for the current environment)
                    blocks.append([ groups[1], match.end(), len(tex_str) ])

            # otherwise it's "end"
            else:
                # pop name off stack (and check that it co-incides with groups[1] )
                assert groups[1] == stack.pop()
                # extend slices only if it's the end of level-one environment
                if len(stack) == 0:
                    # set end_idx of current slice
                    blocks[-1][2] = match.start()
                    # append new 'tex' slice (to cap off this environment)
                    blocks.append([ 'tex', match.end(), len(tex_str) ])
        
        #-----------------------------
        # part 2: process block list and create tree nodes (recursive calls here)
        #-----------------------------
        children = []

        # iterate through blocks
        for block in blocks:

            # init local variables (descriptive names)
            block_name = block[0]
            start_index = block[1]
            end_index = block[2]
            content = tex_str[ start_index:end_index  ]
            
            # tex block (dump content)
            if block_name == 'tex':
                node = TexNode( content )
            
            # lists (handled by parse_list_contents)
            elif block_name in node_types['list']:
                
                classname = doctree_class['list'][block_name]
                node = classname()
                # node = doctree_class['list'][block_name]()
                list_number = node.number
                item_name = item_dict[block_name] # string
                node.children = self.parse_list_contents(content, list_number=list_number, item_name=item_name)
            
            # theorems
            elif block_name in node_types['theorem']:
                classname = doctree_class['theorem'][block_name]
                node = classname()
                node.children = self.parse_block( content )
            
            # exercises
            elif block_name in node_types['exercise']:
                classname = doctree_class['exercise'][block_name]
                node = classname()
                node.children = self.parse_block( content ) 
            
            # boxes
            elif block_name in node_types['box']:
                classname = doctree_class['box'][block_name]
                node = classname()
                node.children = self.parse_block( content ) 
            
            # floats
            elif block_name in node_types['float']:
                classname = doctree_class['float'][block_name]
                node = classname()
                match = re.compile(r'\\caption\{([^\}]+)\}').search(content)
                if match:
                    node.title = match.groups()[0] 
                # source file (figures only)
                if block_name == 'figure':
                    match = re.compile(r'\\includegraphics(\[[^\]]*\])\{([^\}]+)\}').search(content)
                    if match:
                        node.src = match.groups()[1] 
            
            # ignored blocks (need to put back the "begin" and "end")
            elif block_name in node_types['ignored']:
                node = TexNode( r'\begin{%s}%s\end{%s}' % (block_name, content, block_name ))

            # unlisted blocks (do not parse further)
            # delete these in production version
            else:
                node = TexNode( content )

            
            # record start_index and end_index of content (do we need this?)
            node.start_index = start_index
            node.end_index = end_index
            
            # add node to children (with hack to eliminate empty tex nodes)
            if not type(node) == TexNode or node.htex:
                children.append( node )
        
        return children

    #-----------------------------
    # parse list contents
    def parse_list_contents(self, content, list_number=0, item_name="item"):
        '''
        Returns a list of item nodes. These become the only children of the enclosing list node
        The number of enclosing list is passed so that item numbers can be set properly    
        '''
       # find class correpsonding to this type of item
        if item_name in node_types['item']:
            item_class = doctree_class['item'][item_name]
        else:
            return []

        #-----------------------------
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
        tail = content
        while tail:
            block, tail, correct_choice = find_next_item(tail, item_name=item_name)
            item_number = list( list_number ) # copy
            item_number.append(item_counter)
            item_counter += 1
            item = item_class(item_number)
            if type(item) == Choice and correct_choice:
                item.is_correct_choice = True
            item.children = self.parse_block( block )
            item_list.append( item )

        return item_list

    # prettyprint xml tree
    #-----------------------------
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
    },
    'ignored': {
        'equation':    None,
        'align':       None,
        'array':       None,
    },
    'content': {
        'texnode':      TexNode,
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
# read preamble
def read_preamble(filename):
    with open(filename) as f:
        f_str = f.read()
        pattern = r'(.*)\\begin\{document\}' 
        match = re.compile(pattern, re.DOTALL).search( f_str )
        preamble = match.groups()[0] if match else ''
        return preamble

#-----------------------------
# read body
def read_body(filename):
    s = read_latex(filename)
    s = fix_latex(s)
    pattern = r'\\begin{document}(.*)\\end{document}' 
    match = re.compile(pattern, re.DOTALL).search( s )
    body = match.groups()[0] if match else ''
    return body


#-----------------------------
# fix latex (naughty macros)
def fix_latex(s):
    s = re.sub(r'\\bit\s+', r'\\begin{itemize} ', s)
    s = re.sub(r'\\eit\s+', r'\\end{itemize} ', s)
    s = re.sub(r'\\ben\s+', r'\\begin{enumerate} ', s)
    s = re.sub(r'\\een\s+', r'\\end{enumerate} ', s)
    s = re.sub(r'\\it\s+', r'\\item ', s)
    return s

#-----------------------------
# read latex (recurses down through 'input' commands)
def read_latex(filename, level=0):
    if level > 4:
        print('error: read_body: recursion limit reached (max = 4)')
        return ''
        
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
        if not matches:
            return f_str
        else:
            s = ''
            sIdx = 0
            for match in matches:
                eIdx = match.start()
                s += f_str[ sIdx:eIdx ]
                sIdx = match.end()
                nested_filename = match.groups()[0]
                if not re.search(r'\.', nested_filename):
                    nested_filename = nested_filename + '.tex'
                nested_filename = os.path.join(os.path.dirname(filename), nested_filename)
                out.info('File: %s', nested_filename)
                s += read_latex(nested_filename, level=level+1)
            s += f_str[sIdx:]
            return s
        

#-----------------------------
# extract module info
def extract_module_info(main_file):    

    preamble  = read_preamble( main_file )
    minfo = {'year': None, 'code': None, 'title': None}
    
    # year
    match = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
    if match: 
        minfo['year'] = match.groups()[0]

    # code
    match = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
    if match: 
        minfo['code'] = match.groups()[0]

    # title
    match = re.compile(r'\\moduletitle\{(.*)\}').search( preamble )
    if match: 
        minfo['title'] = match.groups()[0]
    
    return minfo
        

#-----------------------------
# extract new commands
def extract_new_commands(main_file):    

    nc = []
    preamble  = read_preamble( main_file )
    pattern = re.compile(r'(\\newcommand\{(\w+)\}\{.*\})') # dodgy
    matches = re.finditer(pattern, preamble)
    for match in matches:
        ncs.append( match.groups()[0] ) 
    return nc
#-----------------------------
# depth-first traversal
# def traverse(node, level=0):
#     if not node.children:
#         if type(node) == TexNode:
#             print node.content
#     else:
#         print '>>>>>>>>>>>>>>>>>>> %d' % len(node.children)
#         # print  node.children
#         for child in node.children:
#             s = 'BEGIN: Node %d (%s)' % (child.node_id, child.__class__.__name__)
#             print '----'*level + s
#             s = 'CHECK: database for object of class %s with node_id %s.' % (child.__class__.__name__, child.node_id)
#             print '----'*level + s
#             traverse(child, level=level+1)
#             s = 'END:   Node %d (%s)' % (child.node_id, child.__class__.__name__)
#             print '----'*level + s
#
#-----------------------------
# extract_labels (recursive)
# def extract_labels(node, level=0):
#     if not node.children:
#         if type(node) == TexNode:
#             print node.content
#     else:
#         print '>>>>>>>>>>>>>>>>>>> %d' % len(node.children)
#         # print  node.children
#         for child in node.children:
#             s = 'BEGIN: Node %d (%s)' % (child.node_id, child.__class__.__name__)
#             print '----'*level + s
#             s = 'CHECK: database for object of class %s with node_id %s.' % (child.__class__.__name__, child.node_id)
#             print '----'*level + s
#             traverse(child, level=level+1)
#             s = 'END:   Node %d (%s)' % (child.node_id, child.__class__.__name__)
#             print '----'*level + s


#-----------------------------
# extract_exercises
# def extract_exercises(node):
#
#     if type(node) == Exercise:
#         print 'Exercise ' + '.'.join(node.number)
#         return [ [node.start_index, node.end_index] ]
#     else:
#         idx_pairs = []
#         for child in node.children:
#            idx_pairs.extend( extract_exercises(child) )
#         return idx_pairs


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

    # build book tree (from input file)
    book = Book( args[0] )

    # text output
    if options.text:
        print book

    # xml output
    if options.xml:
        print book.prettyprint_xml()

    # camel database output
    if options.camel:
        
        # hack to set newcommands
        nc = r'\newcommand{\prob}{\mathbb{P}}'
        nc += r'\newcommand{\expe}{\mathbb{E}}'
        print nc
    
        # extract module information (from main.tex preamble)
        minfo = extract_module_info( args[0] )
        
        # check whether this module already exists in the database
        modules = camel.models.Module.objects.filter(year=minfo['year'], code=minfo['code'])
        if not modules:
            print 'Module does NOT exist in the database...creating it'
            mo = camel.models.Module(year=minfo['year'], code=minfo['code'], title=minfo['title'])
            print mo
            mo.save()
        elif len(modules) > 1:
            print 'More than one module with this year and code exists in the database...PROBLEM!'
            options.commit=False
        else:
            print 'Module DOES exist in the database...book will be hooked on'
            mo = modules[0]
        
        if options.commit:
            mo.newcommands = nc
            mo.save()
            book.camel_tree(module=mo, commit=True)
        else:
            book.camel_tree(module=mo)
          
    # print labels

if __name__ == '__main__':
    main()

