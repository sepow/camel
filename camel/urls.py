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


urlpatterns = patterns('',

    # basic
    url(r'^$', camel.views.index, name='index'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/camel_logo.png')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# content
    url(r'modiwlau/$', camel.views.Module_ListView.as_view(), name='rhestr-modiwlau'),
    url(r'modiwlau/(?P<pk>\d+)/$', camel.views.Module_DetailView.as_view(), name="manylion-modiwl"),
    url(r'treenode/(?P<pk>\d+)/$', camel.views.TreeNode_DetailView.as_view(), name="treenode-detail"),
	url(r'^modules/$', camel.views.module_list, name="module-list"),
    url(r'^(?P<module_code>\w+)/$', camel.views.module_detail, name="module-detail"),
    url(r'^(?P<module_code>\w+)/(?P<chapter_number>\w+)/$', camel.views.chapter_detail, name="chapter-detail"),


    # exercises
    url(r'exercise/(?P<pk>\d+)/$', camel.views.Exercise_DetailView.as_view(), name="exercise-detail"),
    url(r'test/$', camel.views.test, name='test'),
    url(r'quiz/$', camel.views.quiz, name='quiz'),
    url(r'decision/$', camel.views.decision, name='decision'),

    
	# students
	#url(r'^(?P<username>\w+)/$', camel.views.account, name="account"),
	
	# users 
	url(r'^login/$', camel.views.login_view, name="login"),
    url(r'^logout/$', camel.views.logout_view, name="logout"),

   
)
