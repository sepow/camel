'''
camel: admin.py
'''
from django.contrib import admin

from django.contrib.auth.models import User
from camel.models import Module, TreeNode

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'last_name', 'first_name','email')
	ordering = ('username',)

class ModuleAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'year')
	ordering = ('code', 'year',)

class TreeNodeAdmin(admin.ModelAdmin):
	list_display = ('pk','mpath','label','node_type','number','title','htex')
	ordering = ('mpath',)

admin.site.register(Module, ModuleAdmin)
admin.site.register(TreeNode, TreeNodeAdmin)

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
