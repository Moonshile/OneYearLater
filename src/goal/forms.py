
from django import forms
from forever import const
import re, datetime

class GoalForm(forms.Form):
    content = forms.CharField()
    email = forms.EmailField()
    birthday = forms.DateField(required=False)
    gender = forms.NullBooleanField(required=False)

    def clean_content(self):
        content = self.cleaned_data['content']
        length = len(content)
        if length >= 1 and length <= 1000 and not const.PT_BLANK.match(content):
            return content
        raise forms.ValidationError(_('content'))

    def clean_birthday(self):
        today = datetime.date.today()
        oldest = today - datetime.timedelta(days = const.OLDEST)
        birthday = self.cleaned_data['birthday']
        if birthday is None or birthday > oldest and birthday < today:
            return birthday
        raise forms.ValidationError(_('birthday'))

