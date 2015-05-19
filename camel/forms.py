'''
camel: forms.py
'''

from django import forms
from django.contrib.auth.models import User

from django.forms.models import modelformset_factory

from camel.models import Module, TreeNode, Answer, MultipleChoiceAnswer, Submission
# from camel.marker import Report

# answer form (single textarea)
# class AnswerForm(forms.ModelForm):
#     tex_str  = forms.CharField( widget=forms.Textarea( attrs={'rows':16, 'cols':75} ) )
#     class Meta:
#         model = Answer
#         fields = ['question', 'user', 'tex_str', 'submitted']
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'user', 'text', 'readonly']
        widgets = {
            'question': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={'cols': '64', 'id': 'answer-text', 'required': True, 'placeholder': 'Type answer here...'}
            ),
            'readonly': forms.CheckboxInput(attrs={'label': 'readonly'}),
        }

AnswerFormSet = modelformset_factory(
    Answer, 
    form=AnswerForm,
    extra=0,
)

# class QuestionForm(forms.Form):
#     qutestion title = forms.CharField()
#
# QuestionFormSet = formset_factory(
#
#
# )

class SubmitExerciseForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['user', 'assessment', 'declaration']
        widgets = {
            'user': forms.HiddenInput(),
            'assessment': forms.HiddenInput(),
            'declaration': forms.CheckboxInput(),
        }

class MultipleChoiceAnswerForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=[])
    class Meta:
        model = MultipleChoiceAnswer
        fields = ['student', 'submission', 'question', 'answer']

class UserForm(forms.ModelForm):
	password = forms.CharField( widget=forms.PasswordInput() )
	class Meta:
		model = User
		fields = ('username', 'email', 'password')


# # formsets
# from django.forms.formsets import formset_factory
# AnswerFormSet = formset_factory(AnswerForm)
        
