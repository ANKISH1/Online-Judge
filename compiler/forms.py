from django import forms

from compiler.models import CodeSubmission

Language_CHOICES = [
    {"py", "Python"},
    {"c", "C"},
    {"cpp", "C++"},
]

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=Language_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]