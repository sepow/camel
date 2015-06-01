# -*- coding: utf-8 -*-
'''
camel: views.py
'''

# for quizzes etc.
import random

# forms
from django import forms
from django.forms.models import formset_factory, modelformset_factory

# http
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# model-based views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

# misc
from django.utils.decorators import method_decorator

# camel
from camel.models import Module, Book, BookNode, Label, Answer, MultipleChoiceAnswer, Submission
from camel.forms import AnswerForm, UserForm, SubmissionForm
# from camel.forms import MultipleChoiceAnswerForm

#--------------------
# basic
#--------------------
# site homepage
def index(request):
    return render(request, 'index.html', {})


#--------------------
# model-based views
#--------------------
class Module_ListView(ListView):
    model = Module
    context_object_name="module_list"
    template_name = 'module_list.html'
    queryset = Module.objects.order_by('year','code')

class Module_DetailView(DetailView):
    model = Module
    template_name = 'module_detail.html'
    def get_context_data(self, **kwargs):
        context = super(Module_DetailView, self).get_context_data(**kwargs)
        module = self.get_object()
        context['module'] = module
        context['books'] = Book.objects.filter(module=module.id).order_by('number')
        context['next'] = module.get_next()
        context['prev'] = module.get_prev()
        context['toc'] = Module.objects.all().order_by('code')
        return context

class Book_DetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    def get_context_data(self, **kwargs):
        context = super(Book_DetailView, self).get_context_data(**kwargs)
        book = self.get_object()
        context['book'] = book
        context['module'] = book.module
        context['chapters'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=book.tree.mpath )
        context['next'] = book.get_next()
        context['prev'] = book.get_prev()
        context['toc'] = Book.objects.filter(module=book.module.id).order_by('number')
        return context

class Chapter_DetailView(DetailView):
    model = BookNode
    template_name = 'chapter_detail.html'
    def get_context_data(self, **kwargs):
        context = super(Chapter_DetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()
        context['module']  = Module.objects.get( code=chapter.mpath[:6] )
        context['book']  = Book.objects.get( tree=chapter.get_root_node() )
        context['chapter'] = chapter
        context['subtree'] = chapter.get_descendants(include_self=True)
        context['toc'] = chapter.get_siblings(include_self=True)
        context['next'] = chapter.get_next()
        context['prev'] = chapter.get_prev()
        return context

class BookNode_DetailView(DetailView):
    model = BookNode
    template_name = 'booknode_detail.html'
    # def get_success_url(self):
    #     return reverse('chapter-list')
    def get_context_data(self, **kwargs):
        context = super(BookNode_DetailView, self).get_context_data(**kwargs)
        subtree = self.get_object().get_descendants(include_self=True)
        mcode = self.get_object().mpath[:6]
        module = get_object_or_404(Module, code=mcode)
        context['module']  = module
        context['subtree']  = subtree
        chapter = self.get_parent_chapter()
        context['chapter']  = chapter
        context['toc']  = Book.objects.filter( module=module )
        context['next'] = self.get_object().get_next()
        context['prev'] = self.get_object().get_prev()
        return context

# the following should be implemented with javascript on the client
def theorems(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    context['chapter']  = chapter
    qset = BookNode.objects.filter(node_class="theorem", mpath__startswith=chapter.mpath ).order_by('mpath')
    qset = qset.exclude(node_type="example").exclude(node_type="exercise")
    context['blocks'] = qset
    context['blocktype'] = 'theorem'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)

def examples(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    qset = BookNode.objects.filter(node_type="example", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'example'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)

def exercises(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    qset = BookNode.objects.filter(node_type="exercise", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'exercise'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)

def assignments(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    qset = BookNode.objects.filter(node_class="assignment", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'assignment'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)


# edit answer form
@login_required
def edit_answer(request, pk):
    context = RequestContext(request)
    qu = BookNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=qu.mpath[:6] )
    context['book']  = Book.objects.get( tree=qu.get_root_node() )
    context['question'] = qu
    context['subtree'] = qu.get_descendants(include_self=True)
    context['chapter'] = qu.get_parent_chapter()
    context['assignment'] = qu.get_parent_assignment()
    context['toc'] = qu.get_siblings(include_self=True)

    # navigation
    questions = BookNode.objects.filter( node_type="question", mpath__startswith=qu.mpath[:12] ).order_by('mpath')
    next = questions.filter( mpath__gt=qu.mpath )
    prev = questions.filter( mpath__lt=qu.mpath ).order_by('-pk')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None
    
	# answer form 
    # retreive current saved answer (if any)
    ans = Answer.objects.filter(question=qu, user=request.user).first()
    if ans:
        form = AnswerForm(instance=ans)
    else:
        form = AnswerForm( initial={'question': qu, 'user': request.user})

    # gulp
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['question']
            user = form.cleaned_data['user']
            
            # search for saved answer
            answer = Answer.objects.filter(question=ques, user=user).first()
            
            # create new answer if required
            if not answer:
                answer = form.save(commit=False)
                answer.save()
                
            # switch on button pressed
            if 'save-answer' in request.POST:
                answer.text = form.cleaned_data['text']
                answer.is_readonly = form.cleaned_data['is_readonly']
                answer.save()

            elif 'save-and-exit' in request.POST:
                answer.text = form.cleaned_data['text']
                answer.is_readonly = form.cleaned_data['is_readonly']
                answer.save()
                return HttpResponseRedirect( reverse('homework', kwargs={'pk': ques.get_parent_assignment().id}) )

            elif 'exit' in request.POST:
                return HttpResponseRedirect( reverse('homework', kwargs={'pk': ques.get_parent_assignment().id}) )

            else:
                print "BAD LUCK"

        else:
            print "FORM INVALID"
            context['debug'] = form.errors

    context['form'] = form
    return render(request, 'edit_answer.html', context)

# single choice test
@login_required
def sctest(request, pk):
    context = RequestContext(request)
    test = BookNode.objects.get(pk=pk)
    chapter = test.get_parent_chapter()
    questions = BookNode.objects.filter(node_type='question', mpath__startswith=test.mpath).order_by('mpath')

    context['module']  = get_object_or_404( Module, code=test.mpath[:6] )
    context['test'] = test
    context['chapter'] = chapter
    context['questions'] = questions
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    context['toc'] = BookNode.objects.filter( node_type="homework", mpath__startswith=test.mpath[:9] ).order_by('mpath')

    # navigation
    tests = BookNode.objects.filter( node_type="multiplechoice", mpath__startswith=test.mpath[:9] ).order_by('mpath')
    next = tests.filter( mpath__gt=test.mpath )
    prev = tests.filter( mpath__lt=test.mpath ).order_by('-mpath')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None

    triplets = []

    # create question-choices-answer triplets (answer=None is not yet attempted)
    for qu in questions:
        choices = BookNode.objects.filter( node_type__in=['choice','correctchoice'], mpath__startswith=qu.mpath)
        answer = MultipleChoiceAnswer.objects.filter(user=request.user, question=qu).first() # returns none if not yet attempted
        triplets.append([ qu, choices, answer])

    context['triplets'] = triplets

    # check whether this homework has already been attempted
    submission = Submission.objects.filter(user=request.user, assignment=test).first()
    if submission:
        context['submission'] = submission

    # form: hitch on hidden fields here
    form = SubmissionForm( initial={'user': request.user, 'assignment':test.pk} )
    context['form'] = form

    if request.method == 'POST':
        # deal with form (submit)
        # print request.POST
        form = SubmissionForm(request.POST)
        if form.is_valid():

            # extract chosen answers through raw post data (oops!)
            pairs = dict([ [int(k.split('_')[1]),int(v.split('_')[1])] for k,v in form.data.items() if k[:9] == 'question_'])
            for trip in triplets:
                qu = trip[0]
                ch = trip[1]
                an = trip[2]
                if qu.number in pairs:
                    chno = pairs[qu.number]
                    cho = ch[chno-1]
                    if an:
                        an.delete()
                    an = MultipleChoiceAnswer(user=request.user, question=qu, choice=cho)
                    an.save
                    trip[2] = an
                    
            context["triplets"] = triplets
            form = SubmissionForm( initial={'user': request.user, 'assignment':test.pk} )
            context['form'] = form
            
            if 'submit-test' in request.POST:
                
                # update submission
                submission = form.save(commit=False)
                submission.save()
                # we need to update the answers too
                for answer in form.cleaned_data['answers']:
                    if answer:
                        answer.submission = submission
                        answer.save()
            return render_to_response('sctest.html', context)
            
        else:
            context['debug'] = form.errors
            return render_to_response('index.html', context)
    else: # not POST
        return render_to_response('sctest.html', context)
    
# homework (question set)
@login_required
def homework(request, pk):
    context = RequestContext(request)
    hwk = BookNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=hwk.mpath[:6] )
    context['homework'] = hwk
    # context['subtree'] = ex.get_descendants(include_self=True)
    chapter = hwk.get_parent_chapter()
    context['chapter'] = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    context['toc'] = BookNode.objects.filter( node_type="homework", mpath__startswith=hwk.mpath[:9] ).order_by('mpath')

    # navigation
    module = context['module']
    homeworks = BookNode.objects.filter( node_type="homework", mpath__startswith=hwk.mpath[:9] ).order_by('mpath')
    next = homeworks.filter( mpath__gt=hwk.mpath )
    prev = homeworks.filter( mpath__lt=hwk.mpath ).order_by('-mpath')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None

    questions = BookNode.objects.filter(node_type='question', mpath__startswith=hwk.mpath).order_by('mpath')
    context['questions'] = questions
    answers = []
    
    # create question-answer pairs (answer=None is not yet attempted/saved)
    for qu in questions:
        answers.append( Answer.objects.filter(user=request.user, question=qu).first() )
    context['answers'] = answers
    pairs = zip(questions,answers)
    context['pairs'] = pairs

    # check whether this homework has already been submitted
    sub = Submission.objects.filter(user=request.user, assignment=hwk).first()
    if sub:
        context['submission'] = sub

    # submit form: hitch on hidden fields here
    form = SubmissionForm( initial={'user': request.user, 'assignment':hwk.pk, 'declaraion': False} )
    form.fields['answers'] = answers
    context['form'] = form
    
    if request.method == 'POST':
        # deal with form (submit)
        form = SubmissionForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            if 'submit-homework' in request.POST:
                submission = form.save(commit=False)
                submission.save()
                # for answer in form.cleaned_data['answers']:
                for answer in answers:
                    if answer:
                        answer.submission = submission
                        answer.is_readonly = True
                        answer.save()
            return HttpResponseRedirect( reverse('homework', kwargs={'pk': hwk.id}) )
        else:
            context['debug'] = form.errors
            return render_to_response('index.html', context)
    else: # not POST
        return render_to_response('homework.html', context)
    

def question(request, pk):
    context = RequestContext(request)
    qu = BookNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=qu.mpath[:6] )
    context['question'] = qu
    context['subtree'] = qu.get_descendants(include_self=True)
    context['chapter'] = qu.get_parent_by_type('chapter')
    context['exercise'] = qu.get_parent_by_type('exercise')
    context['toc'] = qu.get_siblings(include_self=True)

    # navigation
    questions = BookNode.objects.filter( node_type="question", mpath__startswith=qu.mpath[:12] ).order_by('mpath')
    next = questions.filter( mpath__gt=qu.mpath )
    prev = questions.filter( mpath__lt=qu.mpath ).order_by('-pk')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None
    
	# answer form 
    # retreive current saved answer (if any)
    ans = Answer.objects.filter(question=qu, user=request.user).first()
    if ans:
        form = AnswerForm(instance=ans)
    else:
        form = AnswerForm( initial={'question': qu, 'user': request.user})

    # gulp
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['question']
            user = form.cleaned_data['user']
            current_answer = Answer.objects.filter(question=ques, user=user).first()
            if current_answer:
                current_answer.text = form.cleaned_data['text']
                current_answer.is_readonly = form.cleaned_data['is_readonly']
                current_answer.save()
            else:
                answer = form.save(commit=False)
                answer.save()
        if 'preview-answer' in request.POST:
            print "PREVIEW"
        elif 'save-answer' in request.POST:
            print "SAVE"
        else:
            print "ANFFODUS"

        
    context['form'] = form
    return render(request, 'question.html', context)

# # ANSWERS
# def saveanswer(request):
#     context = RequestContext(request)
#     print 'BING-A'
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             ques = form.cleaned_data['question']
#             user = form.cleaned_data['user']
#             current_answer = Answer.objects.filter(question=ques, user=user).first()
#             if current_answer:
#                 current_answer.text = form.cleaned_data['text']
#                 current_answer.is_readonly = form.cleaned_data['is_readonly']
#                 current_answer.save()
#             else:
#                 answer = form.save(commit=False)
#                 answer.save()
#             # return HTTPResponseRedirect( reverse('question') )
#             context['question'] = ques
#             context['module']  = Module.objects.get( code=ques.mpath[:6] )
#             return render_to_response('save_success.html', context)
#         else:
#             context['debug'] = form.errors
#             # form = ContactForm(data=request.POST, files=request.FILES)
#             return render_to_response('question.html', context)
#     else: # not POST
#         return render_to_response('question.html', context)
#
#     print 'BING-C'
#     return render(request, 'question.html', context)

# SEARCH
def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        results = BookNode.objects.filter(node_type='chapter', title__icontains=q)
        return render(request, 'search_results.html',
            {'results': results, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
    

# def test(request):
#     context = RequestContext(request)
#     return render(request, 'quiz.html', context)
#
# def module_quiz(request, module):
#     context = RequestContext(request)
#     return render(request, 'index.html', context)
#
# def quiz(request):
#     context = {'uname': 'mrurdd'}
#     questions = BookNode.objects.filter(node_type='question')
#     question = random.choice( questions )
#     context['chapter'] = question.get_parent_by_type('chapter')
#     context['exercise'] = question.get_parent_by_type('exercise')
#     context['question'] = question
#     context['question_tree'] = question.get_descendants(include_self=True)
#     form = AnswerForm()
#     form.fields['question'] = question
#     form.fields['question'].widget = forms.HiddenInput()
#     current_user = request.user
#     print current_user.username
#     if current_user.is_authenticated():
#         print current_user.username
#         form.fields['user'] = current_user
#     print form.fields
#     context['answer_form'] = form
#     return render(request, 'quiz.html', context)
#
#
# def decision(request):
#     if request.method == 'POST':
#         context = {}
#         form = AnswerForm(request.POST)
#
#         print form.data
#         if form.is_valid():
#             question = form.cleaned_data['question']
#             if question:
#
#                 # student answer
#                 user_answer = Answer(
#                     student = None,  # get user name
#                     question = question,
#                     answer  = form.cleaned_data['answer'],
#                     )
#                 context['user_answer'] = user_answer
#
#                 #  camel answer
#                 camel_answer = Answer(
#                     student = None,
#                     question = question,
#                     answer  = None # get from database
#                     )
#                 context['camel_answer'] = camel_answer
#
#
#                 # decide whether the user is correct
#                 if user_answer == camel_answer:
#                     context['decision'] = 'Correct'
#                 else:
#                     context['decision'] = 'Incorrect'
#
#                 # retrieve all answers to this question (posts)
#                 context['all_answers'] = Answers.objects.filter(question=question).order_by('pk')
#             else:
#                 context['message'] = form.data # for debugging
#         else:
#             context['message'] = form.errors
#         print context
#         return render(request, 'decision.html', context)
#     else:
#         form = AnswerForm()
#         return render(request, 'quiz.html', { 'form': form })
#
#
#
# # list of modules
# def module_list(request):
#     modules = Module.objects.all().order_by('code')
#     return render(request, 'modules.html', {'modules': modules})
#
# # list of chapters
# def module_detail(request, module_code):
#     module = get_object_or_404(Module, code=module_code)
#     chapters = BookNode.objects.filter(module=module, node_type='chapter').order_by('node_id')
#     return render(request, 'module_detail.html', {'module': module, 'chapters': chapters})
#
# # showtex
# def chapter_detail(request, module_code, chapter_number):
#     module = get_object_or_404(Module, code=module_code)
#     chapter = BookNode.objects.get(module=module, node_type='chapter', number=chapter_number)
#
#     # table of contents (siblings of current chapter)
#     toc = []
#     chaps = chapter.get_siblings(include_self=True)
#     for chap in chaps:
#         toc.append(chap)
#
#     # subtree (descendants of current chapter)
#     subtree = chapter.get_descendants(include_self=True)
#
#     # search subtree for references
#     labs= [ref.htex for ref in subtree.filter(node_type='reference')]
#     refs = [ BookNode.objects.filter(label=lab)[0] for lab in labs ]
#     print refs
#
#
#     return render(request, 'chapter_detail.html', {'module': module, 'refs': refs, 'toc': toc, 'chapter': chapter, 'subtree': subtree})

#--------------------
# users
#--------------------

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
                return render(request, 'userhome.html', {'pk': user.pk})
                
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Account is inactive.")
        else:
            print "Invalid login details: %s, %s" % (username, password)
            return HttpResponse("Login incorrect.")
    else:
        return render_to_response('login.html', {}, context)

# @login_required
def userhome(request, pk):
    return render(request, 'userhome.html', {})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


