# -*- coding: utf-8 -*-
'''
camel: urls.py
'''
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import camel.views

from django.views.generic import ListView
from models import Module


urlpatterns = patterns('',

    # basic
    url(r'^$', camel.views.index, name='index'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/camel_logo.png')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # quick
    url(r'^publishers/$', ListView.as_view( 
        model=Module,
        context_object_name="module_list",
    )),

    # search
    url(r'^search-form/$', camel.views.search_form),
    url(r'^search/$', camel.views.search),
    url(r'^saveanswer/$', camel.views.saveanswer, name='saveanswer'),

    # interactive
    url(r'test/$', camel.views.test, name='test'),
    url(r'quiz/$', camel.views.quiz, name='quiz'),
    url(r'decision/$', camel.views.decision, name='decision'),

    url(r'quiz/(?P<pk>\d+)/$', camel.views.module_quiz, name="module-quiz"),

    url(r'ques/(?P<pk>\d+)/$', camel.views.question, name="question"),


    url(r'exercise/(?P<pk>\d+)/$', camel.views.exercise, name="exercise"),
    url(r'exercise/submit/$', camel.views.submit_exercise, name='submit-exercise',),

    # single element
    # url(r'assessment/(?P<pk>\d+)/$', camel.views.assessment, name="assessment"),
    # url(r'assessment/submit/$', camel.views.submit_assessment, name='submit-assessment',),
    url(r'answers/new/$', camel.views.edit_answer, name='new-answer',),
    url(r'answers/edit/(?P<pk>\d+)/$', camel.views.edit_answer, name='edit-answer',),

    # chapter elements
    url(r'theorems/(?P<pk>\d+)/$', camel.views.theorems, name="chapter-theorems"),
    url(r'examples/(?P<pk>\d+)/$', camel.views.examples, name="chapter-examples"),
    url(r'exercises/(?P<pk>\d+)/$', camel.views.exercises, name="chapter-exercises"),
    # url(r'assessments/(?P<pk>\d+)/$', camel.views.assessments, name="chapter-assessments"),

	# list views
    url(r'modules/$', camel.views.Module_ListView.as_view(), name='module-list'),
    url(r'chapters/(?P<pk>\d+)/$', camel.views.Chapter_ListView.as_view(), name="chapter-list"),
    url(r'exercises/(?P<pk>\d+)/$', camel.views.Exercise_ListView.as_view(), name="exercise-list"),

	# detail views
    url(r'module/(?P<pk>\d+)/$', camel.views.Module_DetailView.as_view(), name="module-detail"),
    url(r'chapter/(?P<pk>\d+)/$', camel.views.Chapter_DetailView.as_view(), name="chapter-detail"),
    url(r'exer/(?P<pk>\d+)/$', camel.views.Exercise_DetailView.as_view(), name="exercise-detail"),
    url(r'question/(?P<pk>\d+)/$', camel.views.Question_DetailView.as_view(), name="question-detail"),
    url(r'treenode/(?P<pk>\d+)/$', camel.views.TreeNode_DetailView.as_view(), name="treenode-detail"),
    
    url(r'book/(?P<pk>\d+)/$', camel.views.Book_DetailView.as_view(), name="book-detail"),
    
    
    #     url(r'answers/$', camel.views.Answer_ListView.as_view(), name='answer-list'),
    #     url(r'^answer/(?P<pk>\d+)/$', camel.views.Answer_DetailView.as_view(), name='answer',),
    # url(r'^answers/new/$', camel.views.Answer_CreateView.as_view(), name='new-answer',),
    # url(r'^answers/edit/(?P<pk>\d+)/$', camel.views.Answer_EditView.as_view(), name='edit-answer',),

    
    
    # url(r'^modules/$', camel.views.module_list, name="module-list"),
    # url(r'^(?P<module_code>\w+)/quiz$', camel.views.module_detail, name="quiz"),
    # url(r'^(?P<module_code>\w+)/$', camel.views.module_detail, name="module-detail"),
    # url(r'^(?P<module_code>\w+)/(?P<chapter_number>\w+)/$', camel.views.chapter_detail, name="chapter-detail"),


    
	# students
	#url(r'^(?P<username>\w+)/$', camel.views.account, name="account"),
	
	# users 
	url(r'^login/$', camel.views.login_view, name="login"),
    url(r'^logout/$', camel.views.logout_view, name="logout"),

   
)
