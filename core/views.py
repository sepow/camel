# -*- coding: utf-8 -*-

# for quizzes etc.
import random

# forms
from django import forms

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
# from django.utils.decorators import method_decorator

# camel
from core.models import Module, Book, BookNode, Label, Answer, SingleChoiceAnswer, Submission
from core.forms import UserForm, AnswerForm, SubmissionForm
# from camel.forms import SingleChoiceAnswerForm

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
# should use mptt instance methods instead of mpath
def selected(request, pk, node_type):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    context['user']  = request.user

    context['node_type'] = node_type
    if node_type == 'theorem':
        qset = BookNode.objects.filter(node_class="theorem", mpath__startswith=chapter.mpath).order_by('mpath')
    elif node_type == 'test':
        qset = BookNode.objects.filter(node_type__in=['singlechoice','multiplechoice'], mpath__startswith=chapter.mpath).order_by('mpath')
    else:
        qset = BookNode.objects.filter(node_type=node_type, mpath__startswith=chapter.mpath).order_by('mpath')
    context['booknodes'] = qset

    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    return render(request, 'chapter_selected_nodes.html', context)

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
    qset = qset.exclude(node_type="example").exclude(node_type="exercise").exclude(node_type="test").exclude(node_type="homework")
    context['blocks'] = qset
    context['blocktype'] = 'theorem'
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
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    return render(request, 'chapter_blocks.html', context)

def tests(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    qset = BookNode.objects.filter(node_type__in=["singlechoice","multiplechoice"], mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'test'
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    return render(request, 'chapter_blocks.html', context)

def homeworks(request, pk):
    context = RequestContext(request)
    booknode = BookNode.objects.get( pk=pk )
    module  = Module.objects.get( code=booknode.mpath[:6] )
    chapter = BookNode.objects.get( mpath=booknode.mpath[:12] )
    context['module']  = module
    context['chapter']  = chapter
    context['book']  = Book.objects.get( tree=chapter.get_root_node() )
    qset = BookNode.objects.filter(node_type="homework", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'homework'
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
    context['toc'] = BookNode.objects.filter( node_type="homework", mpath__startswith=chapter.mpath ).order_by('mpath')

    # navigation
    tests = BookNode.objects.filter( node_type__in=['singlechoice','multiplechoice'], mpath__startswith=chapter.mpath ).order_by('mpath')
    next = tests.filter( mpath__gt=test.mpath )
    prev = tests.filter( mpath__lt=test.mpath ).order_by('-mpath')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None

    triplets = []

    # create question-choices-answer triplets (answer=None is not yet attempted)
    for qu in questions:
        choices = BookNode.objects.filter( node_type__in=['choice','correctchoice'], mpath__startswith=qu.mpath)
        answer = SingleChoiceAnswer.objects.filter(user=request.user, question=qu).first() # returns none if not yet attempted
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
                    an = SingleChoiceAnswer(user=request.user, question=qu, choice=cho)
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

#--------------------
# users
#--------------------
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

@login_required
def userhome(request, pk):
    return render(request, 'userhome.html', {})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


