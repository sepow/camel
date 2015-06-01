# -*- coding: utf-8 -*-
'''
camel: urls.py
'''
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from camel import settings

import camel.views

from django.views.generic import ListView
from models import Module

urlpatterns = patterns('',

    # basic
    url(r'^$', camel.views.index, name='index'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/camel_logo.png')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # search (testing)
    url(r'^search-form/$', camel.views.search_form),
    url(r'^search/$', camel.views.search),

    # multiple choice
    url(r'sctest/(?P<pk>\d+)/$', camel.views.sctest, name="sctest"),
    # url(r'mctest/(?P<pk>\d+)/$', camel.views.mctest, name="mctest"),

    # homework
    url(r'homework/(?P<pk>\d+)/$', camel.views.homework, name="homework"),
    url(r'answers/new/$', camel.views.edit_answer, name='new-answer',),
    url(r'answers/edit/(?P<pk>\d+)/$', camel.views.edit_answer, name='edit-answer',),

    # show selected node_types (should be done with javascript on client)
    url(r'theorems/(?P<pk>\d+)/$', camel.views.theorems, name="chapter-theorems"),
    url(r'examples/(?P<pk>\d+)/$', camel.views.examples, name="chapter-examples"),
    url(r'exercises/(?P<pk>\d+)/$', camel.views.exercises, name="chapter-exercises"),
    url(r'assignments/(?P<pk>\d+)/$', camel.views.assignments, name="chapter-assignments"),

	# list views
    url(r'modules/$', camel.views.Module_ListView.as_view(), name='module-list'),

	# detail views
    url(r'module/(?P<pk>\d+)/$', camel.views.Module_DetailView.as_view(), name="module-detail"),
    url(r'book/(?P<pk>\d+)/$', camel.views.Book_DetailView.as_view(), name="book-detail"),
    url(r'chapter/(?P<pk>\d+)/$', camel.views.Chapter_DetailView.as_view(), name="chapter-detail"),
    url(r'booknode/(?P<pk>\d+)/$', camel.views.BookNode_DetailView.as_view(), name="booknode-detail"),
    
	# users 
	url(r'^home/(?P<pk>\d+)/$', camel.views.userhome, name="user-home"),
	url(r'^login/$', camel.views.login_view, name="login"),
    url(r'^logout/$', camel.views.logout_view, name="logout"),
   
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    )
    

