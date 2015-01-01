
from django import forms
from forever import const
import re

class GoalForm(forms.Form):
    content = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField(required=False)
    gender = forms.NullBooleanField()

    def clean_content(self):
        content = self.cleaned_data['content']
        length = len(content)
        if length >= 1 and length <= 1000 and not const.PT_BLANK.match(content):
            return content
        raise forms.ValidationError('content')

    def clean_age(self):
        age = self.cleaned_data['age']
        if age is None or age <= const.OLDEST and age >= 0:
            return age
        raise forms.ValidationError('age')

