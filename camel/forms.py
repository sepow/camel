'''
camel: forms.py
'''

from django import forms
from django.contrib.auth.models import User

from camel.models import Module, TreeNode, Answer, Submission
# from camel.marker import Report

# answer form (single textarea, post button)
class AnswerForm(forms.Form):
    # tex_str = forms.CharField( widget=forms.Textarea( attrs={'rows':10, 'cols':40} ) )
    class Meta:
        model = Answer
        fields = ['student', 'submission', 'question', 'answer']

# submmission form (many textareas, submit button)
class SubmissionForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['student', 'exercise']

# user
class UserForm(forms.ModelForm):
	password = forms.CharField( widget=forms.PasswordInput() )
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

