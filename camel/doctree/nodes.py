#!/usr/bin/python
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

class Proof(Box):
    def __init__(self):
        Box.__init__(self)

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
                label_lookup[ match.groups()[1] ] = self.number

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
        s = re.sub(r'\\par',                    r'<br>',s)

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
    


