
from django import forms
from forever import const
import re

class GoalForm(forms.Form):
    content = forms.CharField()
    email = forms.EmailField()

    def clean_content(self):
        content = self.cleaned_data['content']
        length = len(content)
        if length >= 1 and length <= 1000 and not const.PT_BLANK.match(content):
            return content
        raise forms.ValidationError(_('content'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if const.PT_EMAIL.match(email):
            return email
        raise forms.ValidationError(_('email'))

