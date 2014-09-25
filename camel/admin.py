'''
camel: admin.py
'''
from django.contrib import admin
from camel.models import Module, Student, Chapter, Section, Exercise

class ModuleAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'year')
	ordering = ('code', 'year',)

class ChapterAdmin(admin.ModelAdmin):
	list_display = ('module', 'number', 'title')
	ordering = ('module', 'number',)

class SectionAdmin(admin.ModelAdmin):
	list_display = ('number', 'title', 'chapter')
	ordering = ('chapter', 'number',)

admin.site.register(Module, ModuleAdmin)
admin.site.register(Student)

admin.site.register(Chapter, ChapterAdmin)
# admin.site.register(Chapter)
# admin.site.register(Section)
admin.site.register(Section, SectionAdmin)
admin.site.register(Exercise)
