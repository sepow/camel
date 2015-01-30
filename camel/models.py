# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

# import camel.doctree as dt

ACADEMIC_YEARS = (
    ('201415', '2014-15'),
    ('201516', '2015-16'),
)
MODULE_CODES = (
    ('MA0000','MA0000'),
    ('MA1500','MA1500'),
    ('MA2500','MA2500'),
)
USER_TYPES = (
    ('STU','Student'),
    ('STA','Staff'),
)


#------------------------------------------------
# test class
class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'pk': self.pk, })

    class MPTTMeta:
        order_insertion_by = ['name']

#------------------------------------------------
# Module 
class Module(models.Model):
    
    # attributes
    year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
    code = models.CharField(max_length=6, choices=MODULE_CODES)
    title = models.CharField(max_length=100)
    
    # users
    teacher = models.ForeignKey(User, null=True, blank=True, related_name="teacher")
    students = models.ManyToManyField(User, null=True, blank=True, related_name="students")

    # misc
    newcommands = models.CharField(max_length=512)
    twitter_widget_id = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.code
        
    def get_absolute_url(self):
        return reverse('module-detail', kwargs={'module_code': self.code})

    # this allows us to run doctree.py in a django shell
    class Meta:
        app_label = 'camel'
        
#------------------------------------------------
# TreeNode
class TreeNode(MPTTModel):

    # keys
    module = models.ForeignKey(Module)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # nowrite flag
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
    
    class MPTTMeta:
        order_insertion_by = ['node_id']

    def __unicode__(self):
        s = '%4d: %10s' % (self.node_id, self.node_type)
        if self.number: s = s + ': '+ str(self.number)
        if self.title: s = s + ': '+ self.title
        if self.label: s = s + '['+ self.label +']'
        if self.htex: s = s + '  >>>>>'+ self.htex +'<<<<<'
        return s

#------------------------------------------------
# Label
class Label(models.Model):
    module = models.ForeignKey(Module)
    tex_label = models.CharField(max_length=100)
    mpath = models.CharField(max_length=100)

    def __unicode__(self):
        return self.module.__unicode__() + u':' + unicode(self.tex_label) + u':' + unicode(self.mpath)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'module': self.module})

#------------------------------------------------
# Submission
class Submission(models.Model):
    student = models.ForeignKey(User)
    exercise = models.ForeignKey(TreeNode)

# class MultipleChoiceAnswer(models.Model):
#     option = models.ForeignKey(Submission)
    


