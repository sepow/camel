'''
camel: admin.py
'''
from django.contrib import admin

from django.contrib.auth.models import User
from camel.models import Module, Book, Chap, TreeNode, Test, Answer, Submission

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'last_name', 'first_name','email')
	ordering = ('username',)

class ModuleAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'year')
	ordering = ('code', 'year',)

class BookAdmin(admin.ModelAdmin):
	list_display = ('mpath', 'module', 'title', 'author')
	ordering = ('mpath', 'title',)

class ChapAdmin(admin.ModelAdmin):
	list_display = ('mpath', 'number','title')
	ordering = ('mpath',)

class TreeNodeAdmin(admin.ModelAdmin):
	list_display = ('pk','mpath','node_class','node_type','label','number','title','htex')
	ordering = ('mpath',)

class TestAdmin(admin.ModelAdmin):
	list_display = ('pk','mpath','label','node_type','number','title','htex')
	ordering = ('mpath',)

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('mpath', 'number')
	ordering = ('mpath', 'number')

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('pk', 'question', 'user', 'text', 'readonly', 'created', 'updated')
	ordering = ('question', 'user')

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('pk', 'assessment', 'created', 'user', 'declaration')
	ordering = ('created', 'user')

admin.site.register(Module, ModuleAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chap, ChapAdmin)
admin.site.register(TreeNode, TreeNodeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)

# No! adding chapters will screw the latex numbering!!
# class ChapterAdmin(admin.ModelAdmin):
#     list_display = ('module', 'number', 'title')
#     ordering = ('module', 'number',)
#
# class SectionAdmin(admin.ModelAdmin):
#     list_display = ('number', 'title', 'chapter')
#     ordering = ('chapter', 'number',)
# admin.site.register(Chapter, ChapterAdmin)
# admin.site.register(Section, SectionAdmin)
# admin.site.register(Exercise)
