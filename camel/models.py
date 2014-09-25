# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

ACADEMIC_YEARS = (
	('201415', '2014-15'),
	('201516', '2015-16'),
)
MODULE_CODES = (
	('MA0000','MA0000'),
	('MA1500','MA1500'),
	('MA2500','MA2500'),
)
USER_STATUS = (
	('STU','Student'),
	('STA','Staff'),
)

#------------------------------------------------
# Students (Users)
#------------------------------------------------
class Student(models.Model):

	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=10)
	#website = models.URLField(blank=True)
	#picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('student', kwargs={'pk': self.id})



#------------------------------------------------
# Module
#------------------------------------------------
class Module(models.Model):
	code = models.CharField(max_length=6, choices=MODULE_CODES)
	year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
	title = models.CharField(max_length=100)
	twitter_widget_id = models.CharField(max_length=50, null=True, blank=True)
	
	# created = models.DateField(auto_now_add=True) 
	# modified = models.DateField(auto_now=True) 

	students = models.ManyToManyField(Student, null=True, blank=True, related_name="students")
	leader = models.ForeignKey(Student, null=True, blank=True) 

	def __unicode__(self):
		return self.code
		
	def get_absolute_url(self):
		return reverse('module-detail', kwargs={'module_code': self.code})

#------------------------------------------------
# Document Tree
# There is no need to define a "children" array in the Module class, to store the Chapters etc
# Instead, every relevant Chapter object is retreived provided its "module" attribute matches
# The TexNodes must be assembled in order, which can be done using "node_number"
# The node-numbers are set by parsemain(), according to the linear order various (dfs)
# The latex number (chapter, section, exercise, figure, ...) are recorede in the "number" field
#------------------------------------------------
class TreeNode(models.Model):
	node_number = models.PositiveSmallIntegerField()	# set by doctree.py (latex numbering)
	is_readonly = models.BooleanField(default=False)	# set by schedule.py
	
#------------------------------------------------
#class DocumentTree(TreeNode):
#	module = models.ForeignKey(Module)
	
#------------------------------
'''
class Division(TreeNode):
	number = models.PositiveSmallIntegerField()			# set by latex
	title  = models.CharField(max_length=100)
	
class Chapter(Division):
	module = models.ForeignKey(Module)

	def get_absolute_url(self):
		return reverse('chapter-detail', kwargs={'module': self.module, 'number': self.number})
	
	def __unicode__(self):
		return self.module.__unicode__() + u'.' + unicode(self.number)
	
class Section(Division):
	chapter = models.ForeignKey(Chapter)
	
class Subsection(Division):
	section = models.ForeignKey(Section)

class Division(TreeNode):
'''	
class Chapter(TreeNode):
	module = models.ForeignKey(Module)
	number = models.PositiveSmallIntegerField()			# set by latex
	title  = models.CharField(max_length=100)
	# def get_absolute_url(self):
	# 	return reverse('chapter-detail', kwargs={'module': self.module, 'number': self.number})
	
	def __unicode__(self):
		return self.module.__unicode__() + u'.' + unicode(self.number)
	
class Section(TreeNode):
	chapter = models.ForeignKey(Chapter)
	number = models.PositiveSmallIntegerField()			# set by latex
	title  = models.CharField(max_length=100)
	# def get_absolute_url(self):
	# 	return reverse('section-detail', kwargs={'module': self.chapter.module, 'chapter': self.chapter, 'number': self.number})
	
class Subsection(TreeNode):
	section = models.ForeignKey(Section)
	number = models.PositiveSmallIntegerField()			# set by latex
	title  = models.CharField(max_length=100)

#------------------------------
class Exercise(TreeNode):
	
	container = models.ForeignKey(TreeNode, related_name='exercise_container')	# chapter, section, subsection
	number = models.CharField(max_length=10) # e.g. 3.1, 3.2 etc
	
	def get_absolute_url(self):
		return reverse('exercise', kwargs={'pk': self.id})
	
	def get_next(self):
		next = Exercise.objects.filter(id__gt=self.id)
		if next: 
			return next[0] 
		return False
	
	def get_prev(self):
		prev = Exercise.objects.filter(id__lt=self.id).order_by('-pk')
		if prev: 
			return prev[0]
		return False

class Diagnostic(Exercise):
	pass
class Formative(Exercise):
	pass
class Summative(Exercise):
	pass

#------------------------------
class List(TreeNode):
	container = models.ForeignKey(TreeNode, related_name='list_container')
	number = models.PositiveSmallIntegerField()

class Itemize(List):
	pass
class Enumerate(List):
	pass
class Questions(List):
	pass
class Parts(List):
	pass
class Subparts(List):
	pass
class Choices(List):
	pass
class Steps(List):
	pass

#------------------------------
class Item(TreeNode):
	mother = models.ForeignKey(List)
	number = models.PositiveSmallIntegerField()

class Question(Item):
	pass
class Part(Item):
	pass
class Subpart(Item):
	pass
class Choice(Item):
	pass
class Step(Item):
	pass
	
#------------------------------
class TexNode(TreeNode):
	container = models.ForeignKey(TreeNode, related_name='texnode_container')
	tex_str = models.TextField()

#------------------------------------------------
# Submission etc
#------------------------------------------------
class Submission(models.Model):
	student = models.ForeignKey(Student)
	exercise = models.ForeignKey(Exercise)

class Answer(models.Model):
	submission = models.ForeignKey(Submission)

class MultipleChoiceAnswer(models.Model):
	option = models.ForeignKey(Submission)
	


