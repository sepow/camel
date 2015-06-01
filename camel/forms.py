'''
camel: forms.py
'''

from django import forms
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User

from camel.models import Module, BookNode, Label, Answer, MultipleChoiceAnswer, Submission

# from camel.marker import Report



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'user', 'text', 'is_readonly']
        widgets = {
            'question': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={'cols': '64', 'id': 'answer-text', 'required': True, 'placeholder': 'Type answer here...'}
            ),
            'readonly': forms.CheckboxInput(attrs={'label': 'readonly'}),
        }

# class MultipleChoiceAnswerForm(forms.ModelForm):
#     # choices = forms.ModelChoiceField(
#     #     queryset = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#     #     # queryset = queryset,
#     #     empty_label=None,
#     #     # choices = ['a','b'],
#     #     widget = forms.RadioSelect(),
#     # )
#     # choices = forms.ModelChoiceField(
#     #     queryset = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#     #     # queryset = queryset,
#     #     empty_label=None,
#     #     # choices = ['a','b'],
#     #     widget = forms.RadioSelect(),
#     # )
#     # alternatives = forms.ModelChoiceField(
#     #     queryset = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#     #     empty_label=None,
#     #     widget = forms.RadioSelect(),
#     # )
#
#     # def __init__(self, choices=None):
#     #     super.__init__(self)
#
#     # alternatives = forms.ChoiceField(
#     #     choices = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#     #     widget = forms.RadioSelect(),
#     # )
#
#     # alternatives = forms.ModelChoiceField(
#     #     queryset = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#     #     empty_label=None,
#     #     widget = forms.RadioSelect(),
#     # )
#
#     class Meta:
#         model = MultipleChoiceAnswer
#         fields = ['question', 'user', 'choice', 'is_readonly']
#         widgets = {
#             'user': forms.HiddenInput(),        # Fkey to user
#             'question': forms.HiddenInput(),    # FKey to question
#             'choice': forms.HiddenInput(),      # Fkey to choice
#             # 'choice': forms.Textarea(
#             #     attrs={'cols': '64', 'id': 'answer-text', 'required': True, 'placeholder': 'Type answer here...'}
#             # ),
#             # 'choice': forms.ChoiceField(
#             #     widget = forms.RadioSelect(),
#             #     choices = ['a','b']
#             #     # choices = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath')
#             #     # queryset = BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath')
#             # ),
#             'readonly': forms.CheckboxInput(attrs={'label': 'readonly'}),
#         }

# homework submission form (no visible fields)
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['user', 'assignment']
        widgets = {
            'user': forms.HiddenInput(),
            'assignment': forms.HiddenInput(),
        }


# formsets
# from django.forms.formsets import formset_factory
# AnswerFormSet = formset_factory(AnswerForm)

# from django.forms.models import modelformset_factory
#
# MultipleChoiceAnswerFormSet = modelformset_factory(
#     MultipleChoiceAnswer,
#     form=MultipleChoiceAnswerForm,
#     extra=0,
# )
        
