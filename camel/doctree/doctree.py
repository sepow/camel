#!/usr/bin/python
#------------------------------------------------
# doctree.py
#------------------------------------------------
import sys, re
import xml.etree.ElementTree as ET
from xml.dom import minidom

debug = True

labels = dict()
#------------------------------------------------
# classes
#------------------------------------------------
class Node(object):
    counter = 0
    
    def __init__(self):
        self.node_number = Node.counter
        self.number = [ Node.counter ]
        Node.counter += 1
        self.attributes = {}
        self.children = []
        
    def num_str(self):
        return '.'.join([ str(k) for k in self.number ])

    def name_str(self): 
        return  self.__class__.__name__ + ' ' + self.num_str() + ': ' + str(self.attributes)
    
    def __repr__(self, level=0):
        s = '----'*level + self.__class__.__name__ + ' ' + self.num_str() + ': ' + str(self.attributes) + '\n'
        for child in self.children:
            s += child.__repr__(level+1)
        return s
    
    def xml(self):
        if debug:
            self.name_str()
        element = ET.Element(self.__class__.__name__)
        for key, val in self.attributes.iteritems():
            element.set(key, val)
        for child in self.children:
            child_element = child.xml()
            element.append(child_element)
        return element

#-----------------------------
# Block 
# Children of non-leaf nodes must be numbered so that they
# can be returned in the correct order by the database.
# The Block object is just a Node with a "block_number" attached
# Not every Node is a block, e.g. chapter/section/subsection
# Blocks can be TexNodes (leaf) or Environments (branch)
class Block(Node):
    counter = 0
    def __init__(self):
        Node.__init__(self)
        self.number = [Block.counter]
        Block.counter += 1


#-----------------------
# Division (abstract)
class Division(Block):
    def __init__(self, title=None, label=None):
        Block.__init__(self)
        self.attributes['number'] = self.num_str()
        if title:
            self.attributes['title'] = title
        if label:
            self.attributes['label'] = label 

class Chapter(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Chapter.counter += 1
        self.number = [Chapter.counter]
        self.attributes['number'] = self.num_str()
        Section.counter = 0
        Subsection.counter = 0
        Figure.counter = 0
        Table.counter = 0
    
class Section(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Section.counter += 1
        self.number = [Chapter.counter, Section.counter]
        self.attributes['number'] = self.num_str()
        Subsection.counter = 0

class Subsection(Division):
    counter = 0
    def __init__(self, title=None, label=None):
        Division.__init__(self, title, label)
        Subsection.counter += 1
        self.number = [Chapter.counter, Section.counter, Subsection.counter]
        self.attributes['number'] = self.num_str()
    
#-----------------------------
# Exercise 
#-----------------------------
class Exercise(Block):
    counter = 0
    def __init__(self):
        Block.__init__(self)
        Exercise.counter += 1
        self.number = [Chapter.counter, Exercise.counter]
        self.attributes['number'] = self.num_str()
        Question.counter = 0
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

#-----------------------------
# Lists 
#-----------------------------
class List(Block):
    counter = 0
    def __init__(self):
        Block.__init__(self)
        List.counter += 1
        self.number = [List.counter]
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
# Item
#-----------------------------
class Item(Block):
    counter = 0
    def __init__(self, item_number):
        Node.__init__(self)
        Item.counter += 1
        self.number = item_number
        self.attributes['number'] = self.num_str()

class Question(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Question.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter]
        self.attributes['number'] = self.num_str()
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

class Part(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Part.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter]
        self.attributes['number'] = self.num_str()
        Subpart.counter = 0
        Choice.counter = 0

class Subpart(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Subpart.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter, Subpart.counter]
        self.attributes['number'] = self.num_str()
        Choice.counter = 0

class Choice(Item):
    counter = 0
    def __init__(self, item_number):
        Item.__init__(self, item_number)
        Choice.counter += 1
        self.number = [Chapter.counter, Exercise.counter, Question.counter, Part.counter, Subpart.counter, Choice.counter]
        self.attributes['number'] = self.num_str()
        self.attributes['correct'] = "false"

class Step(Item):
    def __init__(self, item_number):
        Item.__init__(self, item_number)


#-----------------------------
# Theorems
#-----------------------------
class Theorem(Block):
    counter = 0
    def __init__(self):
        Node.__init__(self)
        Theorem.counter += 1
        self.number = [Chapter.counter, Theorem.counter]

class Lemma(Theorem):
    def __init__(self):
        Theorem.__init__(self)

class Corollary(Theorem):
    def __init__(self):
        Theorem.__init__(self)

class Definition(Theorem):
    def __init__(self):
        Theorem.__init__(self)

class Remark(Theorem):
    def __init__(self):
        Theorem.__init__(self)


#-----------------------------
# Boxes 
#-----------------------------
class Box(Block):
    def __init__(self):
        Block.__init__(self)

# Proof object should be "attached" to a Theorem object (assign current theorem label to proof, e.g. 3.4)
class Proof(Box):
    def __init__(self):
        Box.__init__(self)

# Answer object should be "attached" to a Question object
class Answer(Box):
    def __init__(self):
        Box.__init__(self)

#-----------------------------
# Floats
#-----------------------------
class Figure(Block):
    counter = 0
    def __init__(self, source='nosource', caption='nocaption'):
        Block.__init__(self)
        Figure.counter += 1
        self.number = [Chapter.counter, Figure.counter]
        self.attributes['number'] = self.num_str()
        self.attributes['source'] = source
        self.attributes['caption'] = caption

class Table(Block):
    counter = 0
    def __init__(self, latex_tabular='nolatex', caption='nocaption'):
        Node.__init__(self)
        Block.counter += 1
        self.number = [Chapter.counter, Table.counter]
        self.attributes['number'] = self.num_str()
        self.attributes['latex_tabular'] = latex_tabular
        self.attributes['caption'] = caption

#-----------------------------
# TexNode (content blocks: partial latex to html translation)
#-----------------------------
class TexNode(Block):
    counter = 0

    def __init__(self, s = None):
        Block.__init__(self)
        self.number = [TexNode.counter]
        TexNode.counter += 1
        
        # check for whitespace only
        if not s or not re.compile(r'\S+',re.DOTALL).search(s):
            self.content = ''
            return
        
        # remove comments (line-by-line)
        lines = s.strip().split('\n')
        for idx in range( len(lines) ):
            lines[idx] = re.sub(r'\%.*$', "", lines[idx])
        s = '\n'.join(lines) + '\n'

        # labels and citations
        pattern = re.compile(r'\\(label|ref|cite)\{([^\}]*)\}')
        matches = re.finditer(pattern, s)
        for match in matches:
            if match.groups()[0] == 'label':
                labels[ match.groups()[1] ] = self.number

        # references  and citations
        s = re.sub(r'\\ref\{([^\}]*)\}', r'<a href="\1">here</a>',s)
        s = re.sub(r'\\cite\{([^\}]*)\}', r'<a href="bib:\1">here</a>',s)

        # fonts
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
        s = re.sub(r'\\par ',                    r'<br>',s)

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
            
        self.content = s
    
    def __repr__(self, level=0):
        s = Node.__repr__(self, level)
        s += self.content
        return s

    def xml(self):
        element = ET.Element(self.__class__.__name__)
        element.text = self.content.strip()
        return element
    
#------------------------------------------------
# parameters: correspondence between latex cmds/envs and camel classes
#------------------------------------------------

# latex environments
class_lookup = {
    'list':     {
        'itemize':      (Itemize,   'item'),
        'enumerate':    (Enumerate, 'item'),
        'questions':    (Questions, 'question'),
        'parts':        (Parts,     'part'),
        'subparts':     (Subparts,  'subpart'),
        'choices':      (Choices,   'choice'),
        'steps':        (Steps,     'step'),
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
        'diagnostic':   Exercise,
        'formative':    Exercise,
        'summative':    Exercise,
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
    },
    'format': {
        'center':       Node,
    },
    'box': {
        'proof':        Proof,
        'answer':       Answer,
    },
    'ignore': {
        'equation':    None,
        'align':       None,
    },
}


#-----------------------------
# TexTree
class TexTree(Node):
    def __init__(self, latex_main_file=None):
        Node.__init__(self)
        self.number = [0]

        self.labels = dict()

        if latex_main_file:
            # open input file
            with open(latex_main_file) as f:
                s = f.read()
            self.parse_preamble(s)
            self.parse_body(s)


    #-----------------------------
    # parse preamble
    #-----------------------------
    def parse_preamble(self, latex_str):

        # specify module attributes to extract
        module_attribute_patterns = (
            ('year', r'\\academicyear\{(.*)\}'),
            ('code', r'\\modulecode\{(\w+)\}'),
            ('title', r'\\moduletitle\{(.*)\}'),
        )

        # extract preamble
        pattern = r'(.*)\\begin\{document\}' 
        match = re.compile(pattern, re.DOTALL).search( latex_str )
        preamble = match.groups()[0] if match else ''

        # test document class (should be "camel" with no options) 
        match = re.compile(r'\\documentclass\{([^\}]+)\}').search( preamble )
        if match and not match.groups()[0] == 'camel':
            print 'error: document class must be "camel"'
        
        # extract module attributes (only those listed in module_attribute_patterns)
        for name, pattern in module_attribute_patterns:
            match = re.compile(pattern).search( preamble )
            if match:
                self.attributes[name] = match.groups()[0]

        # new commands (keep as latex for mathjax to handle) 
        self.newcommands = []
        pattern = re.compile(r'(\\newcommand\{(\w+)\}\{.*\})') # dodgy
        matches = re.finditer(pattern, preamble)
        for match in matches:
            self.newcommands.append( TexNode( match.groups()[0] ) ) 


    #-----------------------------
    # parse body
    #-----------------------------
    def parse_body(self, latex_str):

        # extract document body
        pattern = r'\\begin{document}(.*)\\end{document}' 
        match = re.compile(pattern, re.DOTALL).search( latex_str )
        body = match.groups()[0] if match else ''
    
        # initialise container for the chapters/sections/subsections
        root = Block()

        # find all division commands
        pattern = r'\\(chapter|section|subsection)\{([^\}]*)\}'
        matches = re.finditer(pattern, body)

        # build tree
        start_idx= 0
        stack = []
        stack.append(root)
        for match in matches: 
            name    = match.groups()[0]
            title   = match.groups()[1]
            end_idx = match.start()
            latex_str = body[start_idx:end_idx]

            # This latex_str is the block located *before* the current division command
            # The latex_str located after the last division is processed separately at the end  
            # We process latex_str (may be empty) and append subtree to children of enclosing division
            subtree = Block()
            subtree.children = self.parse_block( latex_str )
            stack[-1].children.append( subtree )

            # chapter/section/subsection: close subsection and append to enclosing section
            if name in ['chapter', 'section', 'subsection']:
                if type(stack[-1]) == Subsection:
                    subsec = stack.pop()
                    stack[-1].children.append(subsec)
                # chapter/section: if necessary, close section and append to enclosing chapter
                if name in ['section', 'chapter']:
                    if type(stack[-1]) == Section:
                        sec = stack.pop()
                        stack[-1].children.append(sec)
                    # chapter: if necessary, close current chapter and append to document root
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

        # clean up (after last match has been processed)
        latex_str = body[start_idx:len(body)]
        subtree = Block()
        subtree.children  = self.parse_block( latex_str )
        last_division = stack.pop()
        last_division.children.append(subtree)
        stack[-1].children.append( last_division )    # append last division to parent

        # pop off enclosing environments until we reach the root
        while len(stack) > 1:
            element = stack.pop()
            stack[-1].children.append(element)

        # acquire children 
        root =  stack.pop()
        self.children = root.children


    #-----------------------------
    # parse_block 
    #-----------------------------
    def parse_block(self, latex_str):

        #--------------------
        # Part 1: slice into alternate tex and env blocks
        #--------------------
        
        # find all environment delimiters
        pattern = r'\\(begin|end)\{(\w+)\}'
        matches = re.finditer(pattern, latex_str)

        # loop over matches
        slices = []
        stack = []
        slices.append([ 'tex', 0, len(latex_str)])
        for match in matches: 
            
            # current match
            groups = match.groups()
            
            # do it
            if groups[0] == 'begin':
                if debug:
                    print 'begin: %s' % groups[1]
                # push name onto stack
                stack.append( groups[1] )
                # extend slices only if level-one environment
                if len(stack) == 1:
                    # set end_idx of previous slice
                    slices[-1][2] = match.start()
                    # append new slice (for this environment)
                    slices.append([ groups[1], match.end(), len(latex_str) ])
            else:
                if debug:
                    print 'end: %s' % groups[1]
                # pop name off stack (check that it co-incides with groups[1] )
                name = stack.pop()
                # extend slices only if end of level-one environment
                if len(stack) == 0:
                    # set end_idx of current slice
                    slices[-1][2] = match.start()
                    # append new 'tex' slice (to cap this environment)
                    slices.append([ 'tex', match.end(), len(latex_str) ])
        
        #--------------------
        # part 2: process slice list (make the recursive calls here)
        children = []

        # iterate through slices
        for slice in slices:
            
            env_name = slice[0]
            content = latex_str[ slice[1]:slice[2] ]
            
            # tex
            if env_name == 'tex':
                node = TexNode( content )
            
            # list
            elif class_lookup['list'].has_key( env_name ):
                classname = class_lookup['list'][env_name][0] # object name
                node = classname()
                lnumber = node.number
                iname = class_lookup['list'][env_name][1] # string
                node.children = self.parse_list_contents(content, listnumber=lnumber, itemname=iname)
            
            # theorems
            elif class_lookup['theorem'].has_key(env_name):
                classname = class_lookup['theorem'][ env_name ]
                node = classname()
                node.children = self.parse_block( content ) 
            
            # exercise
            elif class_lookup['exercise'].has_key(env_name):
                classname = class_lookup['exercise'][ env_name ]
                node = classname()
                node.attributes['type'] = env_name
                node.children = self.parse_block( content ) 
            
            # boxes
            elif class_lookup['box'].has_key(env_name):
                classname = class_lookup['box'][ env_name ]
                node = classname()
                node.children = self.parse_block( content ) 
            
            # floats
            elif class_lookup['float'].has_key( env_name ):
                classname = class_lookup['float'][env_name]
                node = classname()
                # all floats
                match = re.compile(r'\\caption\{([^\}]+)\}').search(content)
                if match:
                    node.attributes['caption'] = match.groups()[0] 
                # figure
                if env_name == 'figure':
                    match = re.compile(r'\\includegraphics(\[[^\]]*\])\{([^\}]+)\}').search(content)
                    if match:
                        node.attributes['source'] = match.groups()[1] 
            
            # ignore (maths)
            elif class_lookup['ignore'].has_key( env_name ):
                node = TexNode( r'\begin{%s}%s\end{%s}' % (env_name, content, env_name ))

            # unlisted (need "ignore" environments, because this strips out the env_name)
            else:
                node = TexNode( content )

            # add node to children
            children.append( node )
        
        return children

    #-----------------------------
    # parse list contents
    #-----------------------------
    def parse_list_contents(self, content, listnumber=0, itemname="item"):
        '''
        returns: a list of nodes, which become the children of the calling environment
        '''

       # find class correpsonding to this type of item
        if class_lookup['item'].has_key(itemname):
            classname = class_lookup['item'][itemname]
        else:
            return []

        # function to skip over environments to find the next item
        def find_next_item(latex_str, itemname='item'):
            
            # hack for correctchoice
            if itemname == 'choice':
                itemname = 'choice|correctchoice'
            
            # find all item tokens and environment delimiters
            pattern = r'\\(' + itemname + r')|\\(begin|end)\{(\w+)\}' 
            matches = re.finditer(pattern, latex_str)
            
            # return if no matches at all 
            if not matches:
                return latex_str, []

            # get first match and check that it's an item
            first_match = matches.next()
            if not first_match.groups()[0]:
                return latex_str, []

            # hack to catch correctchoice
            correctchoice = False
            if first_match.groups()[0] == 'correctchoice':
                correctchoice = True

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
                    if len(stack) == 0:
                        end_idx = match.start()
                        return latex_str[start_idx:end_idx], latex_str[ end_idx:len(latex_str) ], correctchoice

            # on the last item, it goes through to the end
            return latex_str[ start_idx:len(latex_str) ], '', correctchoice


        # initialise list to hold items
        item_list = []
        item_counter = 1
        # chop it up
        tail = content
        while tail:
            block, tail, cc = find_next_item(tail, itemname=itemname)
            item_no = list( listnumber ) # copy
            item_no.append(item_counter)
            item_counter += 1
            item = classname(item_no)
            if type(item) == Choice and cc:
                item.attributes['correct'] = "true"
            item.children = self.parse_block( block )
            item_list.append( item )

        return item_list

    # print xml tree
    def prettyprint_xml(self):
        xml_tree = self.xml()
        xml_str = ET.tostring(xml_tree, 'utf-8')
        xml_rep = minidom.parseString(xml_str)
        return xml_rep.toprettyxml(indent="  ")

#-----------------------------
# tree traversal
#-----------------------------

def traverse(node, level=0):
    if not node.children:
        if type(node) == TexNode:
            print node.content
    else:
        print '>>>>>>>>>>>>>>>>>>> %d' % len(node.children)
        print  node.children
        for child in node.children:
            s = 'BEGIN: Node %d (%s)' % (child.node_number, child.name_str())
            print '----'*level + s
            s = 'CHECK: database for object of class %s with number %s.' % (child.__class__.__name__, child.num_str())
            print '----'*level + s
            traverse(child, level=level+1)
            s = 'END:   Node %d (%s)' % (child.node_number, child.name_str())
            print '----'*level + s
#------------------------------------------------
# main
#------------------------------------------------
def main(args=None):
    
    from optparse import OptionParser
    op = OptionParser()
    (options,args) = op.parse_args()
    if not args:
        print 'usage: $python doctree.py main.tex (camel.cls)'
        return
    latex_main_file = args[0]

    # open input file
    with open(latex_main_file) as f:
        latex_str = f.read()

    # initialise tree 
    #module_tree = parse_main(s)
    tex_tree = TexTree( latex_main_file )

    # get xml tree
    #xml_tree = tex_tree.xml()
    #xml_str = ET.tostring(xml_tree, 'utf-8')
    #xml_rep = minidom.parseString(xml_str)

    # output
    print '==============================================='
    #print tex_tree
    print '==============================================='
    #print xml_rep.toprettyxml(indent="  ")
    print tex_tree.prettyprint_xml()
    print '==============================================='
    print labels
    print '==============================================='

    # traverse
    # traverse(tex_tree)

if __name__ == '__main__':
    main()

'''
doctree.py
'''

'''
textree.py: build document tree from latex file (camel.cls)

    1. latex file -> doc_tree
    2. doc_tree -> django models
    3. django_models -> database objects

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
    division: (chapter|section|subsection)
    translate to <h1 class="chapter"> ... </h1>

    list: (itemize|enumerate|questions|parts|subparts)
    translate to <ul class="itemize"> ... </ul> etc.

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

    item: (item|question|part|subpart|choice|correctchoice|step)
    translate to <li class="question"> ... </li>

'''

