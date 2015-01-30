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

	# modules
	url(r'^modules/$', camel.views.module_list, name="module-list"),
	url(r'^(?P<module_code>\w+)/$', camel.views.module_detail, name="module-detail"),
	url(r'^(?P<module_code>\w+)/(?P<chapter_number>\w+)/$', camel.views.chapter_detail, name="chapter-detail"),
    
	# students
	#url(r'^(?P<username>\w+)/$', camel.views.account, name="account"),
	
	# users 
	url(r'^login/$', camel.views.login_view, name="login"),
    url(r'^logout/$', camel.views.logout_view, name="logout"),

   
)
