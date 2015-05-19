# -*- coding: utf-8 -*-
'''
camel: views.py
'''

import random

from django import forms
# from django.forms.models import modelformset_factory

from django.http import HttpResponseRedirect, HttpResponse


from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.views.generic import ListView, DetailView

from django.contrib.auth.models import User
from camel.models import Module, TreeNode, Book, Answer
from camel.forms import AnswerForm, MultipleChoiceAnswerForm, UserForm, AnswerFormSet, SubmitExerciseForm

# import camel.marker as marker
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse, reverse_lazy

# module list
class Module_ListView(ListView):
    model = Module
    context_object_name="module_list"
    template_name = 'module_list.html'
    # queryset = Module.objects.order_by('code')
    # paginate_by = 10
    # success_url = reverse_lazy('module-list')
    # def get_success_url(self):
    #     return reverse(OrderView.plain_view)
    # def get_context_data(self, **kwargs):
    #     context = super(Module_ListView, self).get_context_data(**kwargs)
    #     context['modules'] = Module.objects.order_by('code')
    #     return context

# module detail
class Module_DetailView(DetailView):
    model = Module
    # context_object_name="module"
    template_name = 'chapter_list.html'
    # def get_success_url(self):
    #     return reverse('module-list')
    def get_context_data(self, **kwargs):
        context = super(Module_DetailView, self).get_context_data(**kwargs)
        module = self.get_object()
        context['module'] = module
        context['chapters'] = TreeNode.objects.filter(module=module.id, node_type='chapter').order_by('mpath')
        context['next'] = module.get_next()
        context['prev'] = module.get_prev()
        context['toc'] = Module.objects.all().order_by('code')
        return context

# book and its chapters
class Book_DetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    def get_context_data(self, **kwargs):
        context = super(Book_DetailView, self).get_context_data(**kwargs)
        context['module']  = self.get_object.module
        context['title']  = self.get_object.title
        context['author']  = self.get_object.author
        context['chapters']  = self.get_object().get_children()
        context['next'] = self.get_object().get_next()
        context['prev'] = self.get_object().get_prev()
        return context


# document node and all children
class TreeNode_DetailView(DetailView):
    model = TreeNode
    template_name = 'treenode_detail.html'
    # def get_success_url(self):
    #     return reverse('chapter-list')
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
        context['next'] = self.get_object().get_next()
        context['prev'] = self.get_object().get_prev()
        return context

# chapter (and all descendants)
class Chapter_DetailView(DetailView):
    model = TreeNode
    template_name = 'chapter_detail.html'
    def get_context_data(self, **kwargs):
        context = super(Chapter_DetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()
        context['chapter'] = chapter
        context['module']  = Module.objects.get( code=chapter.mpath[:6] )
        context['subtree'] = chapter.get_descendants(include_self=True)
        context['toc'] = chapter.get_siblings(include_self=True)
        context['next'] = chapter.get_next()
        context['prev'] = chapter.get_prev()
        return context

# list of chapters
class Chapter_ListView(ListView):
    model = TreeNode
    template_name = 'chapter_list.html'
    def get_context_data(self, **kwargs):
        context = super(Chapter_ListView, self).get_context_data(**kwargs)

        module = Module.objects.get( pk=self.kwargs['pk'] )
        context['module']  = module
        context['chapters'] = TreeNode.objects.filter( node_type="chapter", mpath__startswith=module.code )
        context['toc'] = Module.objects.all().order_by('code')
        
        return context

# list of exercises (below a certain node)
class Exercise_ListView(ListView):
    model = TreeNode
    template_name = 'exercise_list.html'
    def get_context_data(self, **kwargs):
        context = super(Exercise_ListView, self).get_context_data(**kwargs)
        
        treenode = TreeNode.objects.get( pk=self.kwargs['pk'] )
        chapter = TreeNode.objects.get( mpath=treenode.mpath[:12] )
        context['module']  = chapter.module
        context['chapter']  = chapter
        context['exercises'] = TreeNode.objects.filter( node_type="exercise", mpath__startswith=chapter.mpath ).order_by('mpath')

        # navigation
        context['next'] = chapter.get_next()
        context['prev'] = chapter.get_prev()
        context['toc'] = Module.objects.all().order_by('code')
        return context

# exercise (and all descendants)
class Exercise_DetailView(DetailView):
    model = TreeNode
    template_name = 'exercise_detail.html'

    def get_success_url(self):
        return reverse('exercise-list')

    def get_context_data(self, **kwargs):
        context = super(Exercise_DetailView, self).get_context_data(**kwargs)

        exercise = self.get_object()
        context['exercise'] = exercise
        context['module']  = get_object_or_404( Module, code=exercise.mpath[:6] )
        context['chapter'] = get_object_or_404( TreeNode, mpath=exercise.mpath[:12] )
        context['subtree'] = exercise.get_descendants(include_self=True)

        # navigation
        module = context['module']
        exercises = TreeNode.objects.filter( node_type="exercise", mpath__startswith=module.code ).order_by('mpath')
        next = exercises.filter( mpath__gt=exercise.mpath )
        prev = exercises.filter( mpath__lt=exercise.mpath ).order_by('-pk')
        context['toc'] = exercises
        context['next'] = next[0] if next else None
        context['prev'] = prev[0] if prev else None

        return context

class Question_DetailView(DetailView):
    model = TreeNode
    template_name = 'question_detail.html'
    def get_success_url(self):
        return reverse('exercise-detail')
    def get_context_data(self, **kwargs):
        context = super(Question_DetailView, self).get_context_data(**kwargs)
        question = self.get_object()
        print '>>>>>>>>>> ' + question.mpath
        context['module']  = get_object_or_404( Module, code=question.mpath[:6] )
        context['book']    = get_object_or_404( TreeNode, mpath=question.mpath[:9] )
        context['chapter'] = question.get_parent_by_type('chapter')
        context['exercise'] = question.get_parent_by_type('exercise')
        context['question'] = question
        context['subtree'] = question.get_descendants(include_self=True)

        # navigation
        exercise = context["exercise"]
        questions = TreeNode.objects.filter( node_type="question", mpath__startswith=exercise.mpath ).order_by('mpath')
        next = questions.filter( mpath__gt=exercise.mpath )
        prev = questions.filter( mpath__lt=exercise.mpath ).order_by('-pk')
        context['toc'] = questions
        context['next'] = next[0] if next else None
        context['prev'] = prev[0] if prev else None
        
    	# answer form
        form = AnswerForm()
        form.fields['question'] = self.get_object()
        context['answer_form'] = form
        
        print context
        return context

def theorems(request, pk):
    context = RequestContext(request)
    treenode = TreeNode.objects.get( pk=pk )
    chapter = TreeNode.objects.get( mpath=treenode.mpath[:12] )
    context['module']  = chapter.module
    context['chapter']  = chapter
    
    qset = TreeNode.objects.filter(node_class="theorem", mpath__startswith=chapter.mpath ).order_by('mpath')
    qset = qset.exclude(node_type="example")
    context['blocks'] = qset
    context['blocktype'] = 'theorem'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = TreeNode.objects.filter( node_type="chapter", module=chapter.module).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)

def examples(request, pk):
    context = RequestContext(request)
    treenode = TreeNode.objects.get( pk=pk )
    chapter = TreeNode.objects.get( mpath=treenode.mpath[:12] )
    context['module']  = chapter.module
    context['chapter']  = chapter
    qset = TreeNode.objects.filter(node_type="example", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'example'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = TreeNode.objects.filter( node_type="chapter", module=chapter.module).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)

def exercises(request, pk):
    context = RequestContext(request)
    treenode = TreeNode.objects.get( pk=pk )
    chapter = TreeNode.objects.get( mpath=treenode.mpath[:12] )
    context['module']  = chapter.module
    context['chapter']  = chapter
    qset = TreeNode.objects.filter(node_type="exercise", mpath__startswith=chapter.mpath ).order_by('mpath')
    context['blocks'] = qset
    context['blocktype'] = 'exercise'

    # navigation
    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = TreeNode.objects.filter( node_type="chapter", module=chapter.module).order_by('mpath')
    
    return render(request, 'chapter_blocks.html', context)


# class Answer_ListView(ListView):
#     model = Answer
#     template_name = 'answers.html'
#     queryset = Answer.objects.order_by('user')
#     paginate_by = 10
#     success_url = reverse_lazy('answer-list')
#     def get_success_url(self):
#         return reverse(OrderView.plain_view)
#
# class Answer_CreateView(CreateView):
#     model = Answer
#     template_name = 'edit_answer.html'
#     def get_success_url(self):
#         return reverse('exercise-detail')
#     def get_context_data(self, **kwargs):
#         context = super(Answer_CreateView, self).get_context_data(**kwargs)
#         context['action'] = reverse('new-answer')
#         return context
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(Answer_EditView, self).dispatch(*args, **kwargs)
#
# class Answer_UpdateView(UpdateView):
#     model = Answer
#     # form_class = AnswerForm
#     template_name = 'edit_answer.html'
#     def get_success_url(self):
#         return reverse('exercise-detail')
#     def get_context_data(self, **kwargs):
#         context = super(Answer_UpdateView, self).get_context_data(**kwargs)
#         context['action'] = reverse('edit-answer', kwargs={'pk': self.get_object().id})
#         return context
#
# class Answer_EditView(UpdateView):
#     model = Answer
#     template_name = 'edit_answer.html'
#
#     def get_success_url(self):
#         return reverse('edit-answer', kwargs={'pk': self.get_object().id})
#
#     def get_context_data(self, **kwargs):
#         context = super(Answer_EditView, self).get_context_data(**kwargs)
#         context['action'] = reverse('edit-answer', kwargs={'pk': self.get_object().id})
#         return context
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(Answer_EditView, self).dispatch(*args, **kwargs)
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.created_by = self.request.user
#         obj.save()
#         return http.HttpResponseRedirect(self.get_success_url())

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         print 'Hello<<<'
    #         return HttpResponseRedirect('/success/')
    #
    #     return render(request, self.template_name, {'form': form})

# class Answer_DeleteView(DeleteView):
#     model = Answer
#     template_name = 'delete_answer.html'
#     def get_success_url(self):
#         return reverse('exercise-detail')


def edit_answer(request, pk):
    context = RequestContext(request)
    qu = TreeNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=qu.mpath[:6] )
    context['question'] = qu
    context['subtree'] = qu.get_descendants(include_self=True)
    context['chapter'] = qu.get_parent_by_type('chapter')
    context['exercise'] = qu.get_parent_by_type('exercise')
    context['toc'] = qu.get_siblings(include_self=True)

    # navigation
    questions = TreeNode.objects.filter( node_type="question", mpath__startswith=qu.mpath[:12] ).order_by('mpath')
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
            answer = Answer.objects.filter(question=ques, user=user).first()
            if not answer:
                answer = form.save(commit=False)
                answer.save()
            if 'save-answer' in request.POST:
                answer.text = form.cleaned_data['text']
                answer.readonly = form.cleaned_data['readonly']
                answer.save()
            elif 'save-and-exit' in request.POST:
                answer.text = form.cleaned_data['text']
                answer.readonly = form.cleaned_data['readonly']
                answer.save()
                return HttpResponseRedirect( reverse('exercise', kwargs={'pk': ques.get_parent_exercise().id}) )
            elif 'exit' in request.POST:
                return HttpResponseRedirect( reverse('exercise', kwargs={'pk': ques.get_parent_exercise().id}) )
            else:
                print "ANFFODUS"
        else:
            print "FORM INVALID"
            context['debug'] = form.errors

    context['form'] = form
    return render(request, 'edit_answer.html', context)

@login_required
def exercise(request, pk):
    context = RequestContext(request)
    ex = TreeNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=ex.mpath[:6] )
    context['exercise'] = ex
    # context['subtree'] = ex.get_descendants(include_self=True)
    context['chapter'] = ex.get_parent_chapter()
    context['toc'] = TreeNode.objects.filter( node_type="exercise", mpath__startswith=ex.mpath[:6] ).order_by('mpath')

    # navigation
    module = context['module']
    exercises = TreeNode.objects.filter( node_type="exercise", mpath__startswith=module.code ).order_by('mpath')
    next = exercises.filter( mpath__gt=ex.mpath )
    prev = exercises.filter( mpath__lt=ex.mpath ).order_by('-pk')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None

    questions = TreeNode.objects.filter(node_type='question', mpath__startswith=ex.mpath).order_by('pk')
    context['questions'] = questions
    answers = []
    for qu in questions:
        answers.append( Answer.objects.filter(user=request.user, question=qu).first() )
    context['answers'] = answers
    print answers
    pairs = zip(questions,answers)
    context['pairs'] = pairs

    # submit form: hitch on hidden fields here
    print '----------------------------------->>>'
    ex = context['exercise']
    print ex
    print ex.node_type
    print ex.id
    print ex.pk
    print '----------------------------------->>>'
    form = SubmitExerciseForm( initial={'user': request.user, 'assessment':ex.pk, 'declaraion': False} )
    form.fields['answers'] = answers
    # form.fields['answers'].widget = forms.HiddenInput()
    context['form'] = form
    
    if request.method == 'POST':
        print 'HELLO-1'
        # deal with form (submit)
        form = SubmitExerciseForm(request.POST)
        # form.fields['answers'] = answers
        # form.fields['answers'].widget = forms.HiddenInput()
        # form.fields['user'] = request.user
        # form.fields['user'].widget = forms.HiddenInput()
        print '-----------------------------------'
        print request.POST
        print '-----------------------------------**'
        print answers
        print '-----------------------------------'
        if form.is_valid():
            print form.cleaned_data
            if 'submit-exercise' in request.POST:
                submission = form.save(commit=False)
                submission.save()
                # for answer in form.cleaned_data['answers']:
                for answer in answers:
                    print '>>>>>>>>>>'
                    print answer
                    print '>>>>>>>>>>'
                    if answer:
                        answer.submission = submission
                        answer.readonly = True
                        answer.save()
                print 'XXXXXXXXXXXXXXXXXX'
            return HttpResponseRedirect( reverse('exercise', kwargs={'pk': ex.id}) )
        else:
            print '00000000000000000000000000'
            context['debug'] = form.errors
            return render_to_response('index.html', context)
    else: # not POST
        return render_to_response('exercise.html', context)
    
    return render(request, 'exercise.html', context)

def submit_exercise(request):
    context = RequestContext(request)
    print 'BING-1'
    if request.method == 'POST':
        print 'BING-2'
        # deal with form (submit)
        form = SubmitExerciseForm(request.POST)
        print '-----------------------------------'
        print form.fields
        print '-----------------------------------'
        if form.is_valid():
            print form.cleaned_data
            answers = form.cleaned_data['answers']
            
            # do something.
            print 'XXXXXXXXXXXXXXXXXX'
        else:
            context['debug'] = form.errors
            return render_to_response('index.html', context)
    else: # not POST
        return render_to_response('index.html', context)
    
    print 'BING-C'
    return render(request, 'exercise_submit.html', context)

def question(request, pk):
    context = RequestContext(request)
    qu = TreeNode.objects.get(pk=pk)
    context['module']  = get_object_or_404( Module, code=qu.mpath[:6] )
    context['question'] = qu
    context['subtree'] = qu.get_descendants(include_self=True)
    context['chapter'] = qu.get_parent_by_type('chapter')
    context['exercise'] = qu.get_parent_by_type('exercise')
    context['toc'] = qu.get_siblings(include_self=True)

    # navigation
    questions = TreeNode.objects.filter( node_type="question", mpath__startswith=qu.mpath[:12] ).order_by('mpath')
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
                current_answer.readonly = form.cleaned_data['readonly']
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

# ANSWERS
def saveanswer(request):
    context = RequestContext(request)
    print 'BING-A'
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['question']
            user = form.cleaned_data['user']
            current_answer = Answer.objects.filter(question=ques, user=user).first()
            if current_answer:
                current_answer.text = form.cleaned_data['text']
                current_answer.readonly = form.cleaned_data['readonly']
                current_answer.save()
            else:
                answer = form.save(commit=False)
                answer.save()
            # return HTTPResponseRedirect( reverse('question') )
            context['question'] = ques
            context['module']  = Module.objects.get( code=ques.mpath[:6] )
            return render_to_response('save_success.html', context)
        else:
            context['debug'] = form.errors
            # form = ContactForm(data=request.POST, files=request.FILES)
            return render_to_response('question.html', context)
    else: # not POST
        return render_to_response('question.html', context)
    
    print 'BING-C'
    return render(request, 'question.html', context)

# SEARCH
def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        results = TreeNode.objects.filter(node_type='chapter', title__icontains=q)
        return render(request, 'search_results.html',
            {'results': results, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
    

def test(request):
    context = RequestContext(request)
    return render(request, 'quiz.html', context)

def module_quiz(request, module):
    context = RequestContext(request)
    return render(request, 'index.html', context)

def quiz(request):
    context = {'uname': 'mrurdd'}
    questions = TreeNode.objects.filter(node_type='question')
    question = random.choice( questions )
    context['chapter'] = question.get_parent_by_type('chapter')
    context['exercise'] = question.get_parent_by_type('exercise')
    context['question'] = question
    context['question_tree'] = question.get_descendants(include_self=True)
    form = AnswerForm()
    form.fields['question'] = question
    form.fields['question'].widget = forms.HiddenInput()
    current_user = request.user
    print current_user.username
    if current_user.is_authenticated():
        print current_user.username
        form.fields['user'] = current_user
    print form.fields
    context['answer_form'] = form
    return render(request, 'quiz.html', context)


def decision(request):
    if request.method == 'POST':
        context = {}
        form = AnswerForm(request.POST)
        
        print form.data
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
        print context
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


