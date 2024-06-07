from django import forms
from compiler.models import submission , result

LANGUAGE_CHOICE = [('py', 'python'), ('c', 'c'), ('cpp', 'c++'),]


class SubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE)

    class Meta:
        model = submission
        fields = ['language', 'code', 'input']


class CodeSubmit(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE)
    
    class Meta:
        model = result
        fields = ['language','problemId','code']
        
            
