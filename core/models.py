# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

# these should be moved to settings.py
ACADEMIC_YEARS = (
    ('2014-15', '2014-15'),
    ('2015-16', '2015-16'),
    ('2016-17', '2016-17'),
)
MODULE_CODES = (
    ('MA0000','MA0000'),
    ('MA0003','MA0003'),
    ('MA1234','MA1234'),
    ('MA1501','MA1501'),
)

#------------------------------------------------
# Module

class Module(models.Model):

    # attributes
    year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
    code = models.CharField(max_length=7, choices=MODULE_CODES)
    title = models.CharField(max_length=100, null=True, blank=True)

    # users
    teacher = models.ForeignKey(User, null=True, blank=True, related_name="module_teacher")
    students = models.ManyToManyField(User, null=True, blank=True, related_name="module_students")

    # misc
    twitter_widget_id = models.CharField(max_length=1024, null=True, blank=True)

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


#------------------------------------------------
# BookNode
class BookNode(MPTTModel):

    # keys
    # module = models.ForeignKey(Module)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # attributes
    node_class = models.CharField(max_length=10)
    node_type = models.CharField(max_length=10)
    number = models.PositiveSmallIntegerField(null=True) # latex number (chapter, figure etc)
    title = models.CharField(max_length=100, null=True, blank=False) # title or caption
    is_readonly = models.BooleanField(default=False)    # set by schedule.py (todo)

    # content
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='figure_images', null=True, blank=False)

    # labels
    node_id = models.PositiveSmallIntegerField() # serial number (from booktree.py)
    mpath = models.CharField(max_length=100, null=True) # materialized path (from booktree.py)
    label = models.CharField(max_length=100, null=True, blank=False) #

    def get_absolute_url(self):
        return reverse('booknode-detail', kwargs={'pk': self.pk})

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

    def get_parent_book(self):
        pa = self
        while pa.node_type != 'book':
            pa = pa.parent
        return pa

    def get_parent_chapter(self):
        pa = self
        while pa.node_type != 'chapter':
            pa = pa.parent
        return pa

    # def get_parent_homework(self):
    #     pa = self
    #     while pa.node_class != 'homework':
    #         pa = pa.parent
    #     return pa
    def get_parent_assignment(self):
        pa = self
        while pa.node_class != 'assignment':
            pa = pa.parent
        return pa

    def get_root_node(self):
        pa = self
        while pa.node_type != 'book':
            pa = pa.parent
        return pa

    def get_descendants_inc_self(self):
        return self.get_descendants(include_self=True)

    class MPTTMeta:
        order_insertion_by = ['node_id']

    def __unicode__(self):
        return self.mpath

#------------------------------------------------
# Module
class Book(models.Model):

    # attributes
    module = models.ForeignKey(Module, null=True, blank=True, related_name="book_module")
    number = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    new_commands = models.CharField(max_length=5000, null=True, blank=True)
    tree = models.ForeignKey(BookNode, related_name="book_tree", null=True)

    def __unicode__(self):
        s = ''
        if self.module:
            s += self.module.code
        if self.number:
            s += ' | book ' + str(self.number)
        if self.title:
            s += ' | ' + self.title
        # if self.new_commands:
        #     s += '\n' + self.new_commands
        return unicode(s)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.id})

    def get_next(self):
        nesaf = Book.objects.filter(module=self.module, number__gt=self.number)
        return nesaf[0] if nesaf else None

    def get_prev(self):
        prev = Book.objects.filter(module=self.module, number__lt=self.number).order_by('-number')
        return prev[0] if prev else None


#------------------------------------------------
# Label
class Label(models.Model):
    book = models.ForeignKey(Book)
    text = models.CharField(max_length=100)
    mpath = models.CharField(max_length=1000)

    def __unicode__(self):
        return unicode(self.text) + u' -> ' + unicode(self.mpath)

#------------------------------------------------
# Answer
class Answer(models.Model):

    user = models.ForeignKey(User)
    question = models.ForeignKey(BookNode)
    text = models.TextField()
    is_readonly = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        s = unicode( self.question.mpath )
        s = s + unicode('|' + self.user.username )
        s = s + unicode('|' + self.text )
        s = s + unicode('|' + str(self.is_readonly) )
        return s

class SingleChoiceAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(BookNode)
    choice = models.ForeignKey(BookNode, related_name='mcanswer_choice')
    is_readonly = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        s = self.question.mpath
        s = s + '|' + self.user.username
        s = s + '|' + str(self.choice)
        s = s + '|' + str(self.is_readonly) + '\n'
        return unicode(s)

#------------------------------------------------
# Assessment
class Submission(models.Model):

    user = models.ForeignKey(User)
    assignment = models.ForeignKey(BookNode)
    is_readonly = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']



# class Teacher(models.Model):
#     user = models.OneToOneField(User)
#
#     def __unicode__(self):
#         return self.user.username
#
# class Student(models.Model):
#     user = models.OneToOneField(User)
#
#     def __unicode__(self):
#         return self.user.username
