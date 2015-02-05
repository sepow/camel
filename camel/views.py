# -*- coding: utf-8 -*-
'''
camel: views.py
'''

import random

from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.views.generic import ListView, DetailView

from camel.models import Module, TreeNode
from camel.forms import AnswerForm, SubmissionForm, UserForm

# import camel.marker as marker


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse, reverse_lazy

# list of modules
class Module_ListView(ListView):
    model = Module
    template_name = 'rhestr_modiwlau.html'
    queryset = Module.objects.order_by('code')  
    paginate_by = 10  
    success_url = reverse_lazy('rhestr-modiwlau')
    def get_success_url(self):
        return reverse(OrderView.plain_view)

class Module_DetailView(DetailView):
    model = Module
    template_name = 'manylion_modiwl.html'
    def get_success_url(self):
        return reverse('rhestr-modiwlau')
    def get_context_data(self, **kwargs):
        context = super(Module_DetailView, self).get_context_data(**kwargs)
        # qset = Dadansoddiad.objects.filter(llinell=self.get_object().id).order_by('dadansoddwr')
        # qset = list(qset)
        qset = TreeNode.objects.filter(module=self.get_object().id, node_type='chapter').order_by('mpath')
        context['chapters']  = qset
        # context['next'] = self.get_object().get_next()
        # context['prev'] = self.get_object().get_prev()
        return context

class TreeNode_DetailView(DetailView):
    model = TreeNode
    template_name = 'treenode_detail.html'
    def get_success_url(self):
        return reverse('manylion-modiwl')
    def get_context_data(self, **kwargs):
        context = super(TreeNode_DetailView, self).get_context_data(**kwargs)
        subtree = self.get_object().get_descendants(include_self=True)
        mcode = self.get_object().mpath[:6]
        module = get_object_or_404(Module, code=mcode)
        context['module']  = module
        context['subtree']  = subtree
        chapter = self.get_object()
        while chapter.node_type != 'chapter':
            chapter = chapter.parent
        context['chapter']  = chapter
        context['toc'] = chapter.get_siblings(include_self=True)
        # context['next'] = self.get_object().get_next()
        # context['prev'] = self.get_object().get_prev()
        return context

class Exercise_DetailView(DetailView):
    model = TreeNode
    template_name = 'exercise_detail.html'
    def get_success_url(self):
        return reverse('manylion-modiwl')
    def get_context_data(self, **kwargs):
        context = super(Exercise_DetailView, self).get_context_data(**kwargs)
        print '>>>>>>>>>> ' + self.get_object().mpath[:10]
        context['module']  = get_object_or_404( Module, code=self.get_object().mpath[:6] )
        context['chapter'] = get_object_or_404( TreeNode, mpath=self.get_object().mpath[:12] )
        context['subtree'] = self.get_object().get_descendants(include_self=True)

        exercises = TreeNode.objects.filter(node_type='exercise')
        next = exercises.filter( mpath__gt=self.get_object().mpath )
        prev = exercises.filter( mpath__lt=self.get_object().mpath ).order_by('-pk')
        context['next'] = next[0] if next else None
        context['prev'] = prev[0] if prev else None

        return context


def test(request):
    context = {'uname': 'mrurdd'}
    return render(request, 'quiz.html', context)

def quiz(request):
    context = {'uname': 'mrurdd'}
    print context
    questions = TreeNode.objects.filter(node_type='question')
    question = random.choice( questions )
    context['question'] = question
    form = AnswerForm( initial={ 'question':question } )
    # form.fields['question'].widget = forms.HiddenInput()
    context['answer_form'] = form
    return render(request, 'quiz.html', context)


def decision(request):
    if request.method == 'POST':
        context = {'uname': 'mrurdd'}
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            question = form.cleaned_data['question']
            if question:
                                
                # student answer
                user_answer = Answer(
                    student = None,  # get user name
                    question = question,
                    answer  = form.cleaned_data['answer'],
                    )
                context['user_answer'] = user_answer
            
                #  camel answer
                camel_answer = Answer(
                    student = None,
                    question = question,
                    answer  = None # get from database
                    )
                context['camel_answer'] = camel_answer


                # decide whether the user is correct
                if user_answer == camel_answer:
                    context['decision'] = 'Correct'
                else:
                    context['decision'] = 'Incorrect'
                    
                # retrieve all answers to this question (posts)
                context['all_answers'] = Answers.objects.filter(question=question).order_by('pk')
            else:
                context['message'] = form.data # for debugging
        else:
            context['message'] = form.errors
        return render(request, 'decision.html', context)
    else:
        form = AnswerForm() 
        return render(request, 'quiz.html', { 'form': form })



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
    
    # search subtree for references
    labs= [ref.htex for ref in subtree.filter(node_type='reference')]
    refs = [ TreeNode.objects.filter(label=lab)[0] for lab in labs ]
    print refs
    
    
    return render(request, 'chapter_detail.html', {'module': module, 'refs': refs, 'toc': toc, 'chapter': chapter, 'subtree': subtree})

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


