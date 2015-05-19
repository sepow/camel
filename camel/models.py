# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

# import camel.doctree as dt
# from camel.doctree import Book as dBook
import camel.doctree as dt

ACADEMIC_YEARS = (
    ('201415', '2014-15'),
    ('201516', '2015-16'),
    ('201617', '2016-17'),
)
MODULE_CODES = (
    ('MA0000','MA0000'),
    ('MA1234','MA1234'),
    ('MA1500','MA1500'),
    ('MA1501','MA1501'),
    ('MA2500','MA2500'),
)
USER_TYPES = (
    ('STU','Student'),
    ('STA','Staff'),
)


# #------------------------------------------------
# # test class
# class Genre(MPTTModel):
#     name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
#
#     def get_absolute_url(self):
#         return reverse('genre_detail', kwargs={'pk': self.pk, })
#
#     class MPTTMeta:
#         order_insertion_by = ['name']

#------------------------------------------------
# Module 
class Module(models.Model):
    
    # attributes
    year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
    code = models.CharField(max_length=6, choices=MODULE_CODES)
    title = models.CharField(max_length=100, null=True, blank=True)
    
    # users
    teacher = models.ForeignKey(User, null=True, blank=True, related_name="teacher")
    students = models.ManyToManyField(User, null=True, blank=True, related_name="students")

    # misc
    newcommands = models.CharField(max_length=1024, null=True, blank=True)
    twitter_widget_id = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.code
        
    # def get_absolute_url(self):
    #     return reverse('module-detail', kwargs={'module_code': self.code})
        
    def get_absolute_url(self):
        return reverse('module-detail', kwargs={'pk': self.id})

    def get_next(self):
        nesaf = Module.objects.filter(code__gt=self.code)
        if nesaf:
            return nesaf[0]
        return None
        
    def get_prev(self):
        prev = Module.objects.filter(code__lt=self.code).order_by('-code')
        if prev:
            return prev[0]
        return None
    

    # this allows us to run doctree.py in a django shell
    class Meta:
        app_label = 'camel'
        
#------------------------------------------------
# TreeNode
class DocumentNode(MPTTModel):

    # keys
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # basic attributes
    node_id = models.PositiveSmallIntegerField()        # serial number (set by doctree.py)
    is_readonly = models.BooleanField(default=False)    # set by schedule.py
    mpath = models.CharField(max_length=100, null=True) # materialized path (set by doctree.py)
    label = models.CharField(max_length=100, null=True, blank=False) # latex label (set by latex source)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    def get_next(self):
        nesaf = self.get_next_sibling()
        if nesaf:
            return nesaf
        return False
        
    def get_prev(self):
        prev = self.get_previous_sibling()
        if prev:
            return prev
        return False
    
#------------------------------------------------
# book
class Book(DocumentNode, dt.Book):
    
    # attributes
    module = models.ForeignKey(Module)
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        s = '%8d: %s' % (self.node_id, self.mpath)
        if self.title: s = s + ': '+ self.title
        if self.author: s = s + ' ['+ self.author + ']'
        return s

#------------------------------------------------
# chap
class Chap(DocumentNode, dt.Chapter):
    
    # attributes
    title = models.CharField(max_length=100, null=True)
    number = models.PositiveSmallIntegerField(null=True) # latex number (chapter, figure etc)

    def get_absolute_url(self):
        return reverse('chapter-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        s = '%8d: %s' % (self.node_id, self.mpath)
        if self.number: s = s + unicode(self.number) + '. '
        if self.title: s = s + self.title
        return s

#------------------------------------------------
# chap
class Figure(DocumentNode, dt.Figure):
    
    # attributes
    caption = models.CharField( max_length=100, null=True )
    number = models.PositiveSmallIntegerField( null=True )
    image = models.ImageField(upload_to='figure_images', null=True, blank=False)

    def __unicode__(self):
        s = '%8d: %s' % (self.node_id, self.mpath)
        if self.number: s = s + unicode(self.number) + '. '
        if self.title: s = s + self.title
        return s

#------------------------------------------------
# TreeNode
class TreeNode(MPTTModel):
    
    # keys
    module = models.ForeignKey(Module)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # read-only flag
    is_readonly = models.BooleanField(default=False)    # set by schedule.py

    # labels
    node_id = models.PositiveSmallIntegerField() # serial number (set by doctree.py)
    mpath = models.CharField(max_length=100, null=True) # materialized path
    label = models.CharField(max_length=100, null=True, blank=False) # latex label

    # attributes
    node_class = models.CharField(max_length=10)
    node_type = models.CharField(max_length=10)
    number = models.PositiveSmallIntegerField(null=True) # latex number (chapter, figure etc)
    title = models.CharField(max_length=100, null=True, blank=False) # title or caption
    
    # content
    htex = models.TextField(null=True)
    image = models.ImageField(upload_to='figure_images', null=True, blank=False)
    
    # misc. 
    is_correct_choice = models.BooleanField(default=False)    # hack


    def get_absolute_url(self):
        return reverse('treenode-detail', kwargs={'pk': self.pk})
    
    def get_next(self):
        nesaf = self.get_next_sibling()
        if nesaf:
            return nesaf
        return False
        
    def get_prev(self):
        prev = self.get_previous_sibling()
        if prev:
            return prev
        return False
    
    def get_parent_by_type(self, node_type):
        pa = self.parent
        while pa.node_type != node_type:
            pa = pa.parent
        return pa

    def get_parent_chapter(self):
        pa = self
        while pa.node_type != 'chapter':
            pa = pa.parent
        return pa

    def get_parent_exercise(self):
        pa = self
        while pa.node_type != 'exercise':
            pa = pa.parent
        return pa

    def get_descendants_inc_self(self):
        return self.get_descendants(include_self=True)

    class MPTTMeta:
        order_insertion_by = ['node_id']

    def __unicode__(self):
        return self.mpath
        # s = '%4d: %10s' % (self.node_id, self.node_type)
        # if self.number: s = s + ': '+ str(self.number)
        # if self.title: s = s + ': '+ self.title
        # if self.label: s = s + '['+ self.label +']'
        # if self.htex: s = s + '  >>>>>'+ self.htex +'<<<<<'
        # return s

class Test(TreeNode):
    pass
    
#------------------------------------------------
# Label (probably not needed - use mpaths instead)
class Label(models.Model):
    module = models.ForeignKey(Module)
    tex_label = models.CharField(max_length=100)
    mpath = models.CharField(max_length=100)

    def __unicode__(self):
        return self.module.__unicode__() + u':' + unicode(self.tex_label) + u':' + unicode(self.mpath)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'module': self.module})

#------------------------------------------------
# Interactive
class Answer(models.Model):
    
    question = models.ForeignKey(TreeNode)
    user = models.ForeignKey(User)
    text = models.TextField()
    readonly = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created']

    def __unicode__(self):
        s = unicode( self.question.mpath )
        s = s + unicode('|' + self.user.username )
        s = s + unicode('|' + self.text )
        return s
#------------------------------------------------
class Submission(models.Model):
    
    user = models.ForeignKey(User)
    assessment = models.ForeignKey(TreeNode, null=True)
    created = models.DateTimeField(auto_now_add=True)    
    declaration = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created']

#------------------------------------------------
class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(TreeNode)
    user = models.ForeignKey(User, null=True, blank=True)
    choice = models.CharField(max_length=1)
    readonly = models.BooleanField(default=False)
    def __unicode__(self):
        return unicode( choice )

    


