# -*- coding: utf-8 -*-
'''
camel: views.py
'''
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView

from camel.models import Module, Chapter, Section

def index(request):
	context = {}
	return render(request, 'index.html', context)

def modules(request):
	modules = Module.objects.all().order_by('code')
	return render(request, 'modules.html', {'modules': modules})

def module_detail(request, module_code):
	module = get_object_or_404(Module, code=module_code)
	chapters = Chapter.objects.filter(module=module).order_by('number')
	context = {'module': module, 'chapters': chapters}
	return render(request, 'module_detail.html', context)

def chapter_detail(request, module_code, chapter_number):
	module = get_object_or_404(Module, code=module_code)
	chapter = get_object_or_404(Chapter, module=module, number=chapter_number)
	sections = Section.objects.filter(chapter=chapter).order_by('number')
	print sections
	context = {'module': module, 'chapter': chapter, 'sections': sections}
	return render(request, 'chapter_detail.html', context)

def section_detail(request, module_code, chapter_number, section_number):
	module = get_object_or_404(Module, code=module_code)
	chapter = get_object_or_404(Chapter, module=module, number=chapter_number)
	section = get_object_or_404(Section, chapter=chapter, number=section_number)
	context = {'module': module, 'chapter': chapter, 'section': section}
	return render(request, 'section_detail.html', context)


#------------------------------
class Module_ListView(ListView):
	model = Module
	template_name = 'module_list.html'
	def get_success_url(self):
		return reverse('module-list')
	def get_context_data(self, **kwargs):
		context = super(Module_ListView, self).get_context_data(**kwargs)
		context['test_attr'] = 'bingo'
		return context


class Module_DetailView(DetailView):
	model = Module
	template_name = 'module_detail.html'
	def get_success_url(self):
		return reverse('module-list')
	# def get_absolute_url(self):
	# 	return reverse("module-detail", kwargs={"code": self.code})
	def get_context_data(self, **kwargs):
		context = super(Module_DetailView, self).get_context_data(**kwargs)
		chapters = Chapter.objects.filter(module=self.get_object().id).order_by('node_number')
		context['chapters']	 = chapters
		return context

#------------------------------
class Chapter_ListView(ListView):
	model = Chapter
	template_name = 'chapter_list.html'
	def get_success_url(self):
		return reverse('module-list')
	def get_context_data(self, **kwargs):
		context = super(Chapter_ListView, self).get_context_data(**kwargs)
		context['test_attr'] = 'xxxxx'
		return context


#------------------------------
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


