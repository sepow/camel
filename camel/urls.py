# -*- coding: utf-8 -*-
'''
camel: urls.py
'''
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import camel.views

urlpatterns = patterns('',

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/camel_logo.png')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', camel.views.index, name='index'),
    
	url(r'module-list/$', camel.views.Module_ListView.as_view(), name='module-list'),
	url(r'chapter-list/$', camel.views.Chapter_ListView.as_view(), name='chapter-list'),
	# url(r'chapter-list/$', camel.views.Section_ListView.as_view(), name='section-list'),
    # url(r'^modules/(?P<pk>\d+)/$', camel.views.Module_DetailView.as_view(), name='module',),
	url(r'modules/$', camel.views.modules, name="modules"),
	#url(r'^(?P<pk>\w+)/$', camel.views.Module_DetailView.as_view(), name="module-detail"),
	url(r'^(?P<module_code>\w+)/$', camel.views.module_detail, name="module-detail"),
	url(r'^(?P<module_code>\w+)/(?P<chapter_number>\d+)/$', camel.views.chapter_detail, name="chapter-detail"),
	url(r'^(?P<module_code>\w+)/(?P<chapter_number>\d+)/(?P<section_number>\d+)$', camel.views.section_detail, name="section-detail"),
   
	# students
	#url(r'^(?P<username>\w+)/$', camel.views.account, name="account"),
	
	# users 
	url(r'^login/$', camel.views.login_view, name='login'),
    url(r'^logout/$', camel.views.logout_view, name='logout'),

)
