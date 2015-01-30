# -*- coding: utf-8 -*-
'''
camel: views.py
'''
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.views.generic import ListView, DetailView

from camel.models import Module, TreeNode


# homepage
def index(request):
	context = {}
	return render(request, 'index.html', context)

# list of modules
def module_list(request):
    modules = Module.objects.all().order_by('code')
    return render(request, 'modules.html', {'modules': modules})

# list of chapters
def module_detail(request, module_code):
    module = get_object_or_404(Module, code=module_code)
    chapters = TreeNode.objects.filter(module=module, node_type='chapter').order_by('node_id')
    return render(request, 'module_detail.html', {'module': module, 'chapters': chapters})

# showtex
def chapter_detail(request, module_code, chapter_number):
    module = get_object_or_404(Module, code=module_code)
    chapter = TreeNode.objects.get(module=module, node_type='chapter', number=chapter_number)

    # table of contents (siblings of current chapter)
    toc = []
    chaps = chapter.get_siblings(include_self=True)
    for chap in chaps:
        toc.append(chap)
    
    # subtree (descendants of current chapter)
    subtree = chapter.get_descendants(include_self=True)
    
    return render(request, 'chapter_detail.html', {'module': module, 'toc': toc, 'chapter': chapter, 'subtree': subtree})

# login
def login_view(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Account is inactive.")
		else:
			print "Invalid login details: %s, %s" % (username, password)
			return HttpResponse("Login incorrect.")
	else:
		return render_to_response('login.html', {}, context)

#------------------------------
@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


