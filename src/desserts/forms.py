#coding=utf-8
from django import forms
from django.contrib.auth.models import User

from models import Activity

import re

max_len_msg = u'不长于%d个字符'
min_len_msg = u'不短于%d个字符'

class AddActivityForm(forms.Form):
    text = forms.CharField(max_length=20, min_length=1, error_messages={
        'max_length': max_len_msg % 20,
        'min_length': min_len_msg % 1,
        'invalid': u'是字母、数字或者汉字',
        'required': u'必须填写内容',
    })

    def clean_text(self):
        pattern = re.compile(r'^.+$')
        text = self.cleaned_data['text']
        if not pattern.match(text):
            raise forms.ValidationError((u'是字母、数字或者汉字'), code='content')
        return text

class RmActivityForm(forms.Form):
    id = forms.IntegerField(error_messages={
        'invalid': u'是数字',
        'required': u'必须填写内容',
    })

    def clean_id(self):
        id = self.cleaned_data['id']
        if Activity.objects.filter(id=id).count() == 0:
            raise forms.ValidationError((u'活动不存在'), code='not_exist')
        return id

class TodoForm(AddActivityForm):
    pass
