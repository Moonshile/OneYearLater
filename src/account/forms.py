#coding=utf-8
from django import forms
from django.contrib.auth.models import User

from models import InvitationCode

import re

max_len_msg = u'不长于%d个字符'
min_len_msg = u'不短于%d个字符'

class SignupForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=3, error_messages={
        'max_length': max_len_msg % 10,
        'min_length': min_len_msg % 3,
        'invalid': u'是字母、数字或者汉字',
    })
    email = forms.EmailField(error_messages={
        'invalid': u'合法的邮箱，如user@abc.com',
    })
    password = forms.CharField(max_length=15, min_length=6, error_messages={
        'max_length': max_len_msg % 15,
        'min_length': min_len_msg % 6,
        'invalid': u'是半角字母、数字或者标点符号',
    })
    password2 = forms.CharField(error_messages={
        'invalid': u'与第一次输入一致',
    })
    """
    invitation_code = forms.CharField(required=False, error_messages={
        'invalid': u'是字母或者数字',
    })
    """

    def clean_username(self):
        pattern = re.compile(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$')
        username = self.cleaned_data['username']
        if not pattern.match(username):
            raise forms.ValidationError((u'是字母、数字或者汉字'), code='content')
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError((u'用户名已经存在'), code='dup_username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError((u'邮箱已经被占用'), code='dup_email')
        return email

    def clean_password(self):
        pattern = re.compile(r'^[\x21-\x7e]+$')
        password = self.cleaned_data['password']
        if not pattern.match(password):
            raise forms.ValidationError((u'是半角字母、数字或者标点符号'), code='content')
        return password

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password = self.data['password']
        if password2 != password:
            raise forms.ValidationError((u'与第一次输入一致'), code='same')
        return password2
    """
    def clean_invitation_code(self):
        invitation_code = self.cleaned_data['invitation_code']
        if InvitationCode.objects.filter(code=invitation_code).count() == 0:
            raise forms.ValidationError((u'邀请码错误'), code='exists')
        raise invitation_code
    """
class SigninForm(forms.Form):
    username = forms.CharField(error_messages={
        'invalid': u'用户名或者邮箱错误',
    })
    password = forms.CharField(max_length=15, min_length=6, error_messages={
        'max_length': max_len_msg % 15,
        'min_length': min_len_msg % 6,
        'invalid': u'是半角字母、数字或者标点符号',
    })

    def clean_username(self):
        pattern = re.compile(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$')
        email = forms.EmailField(error_messages={'invalid': u'是字母、数字或者汉字，或者你的邮箱'})
        username = self.cleaned_data['username']
        if not pattern.match(username) and not email.clean(username):
            raise forms.ValidationError((u'是字母、数字或者汉字，或者你的邮箱'), code='content')
        """
        if User.objects.filter(username=username).count == 0 and User.objects.filter(email=username) == 0:
            raise forms.ValidationError((u'用户名或者邮箱不存在'), code='wrong_user')
        """
        return username

    def clean_password(self):
        pattern = re.compile(r'^[\x21-\x7e]+$')
        password = self.cleaned_data['password']
        if not pattern.match(password):
            raise forms.ValidationError((u'是半角字母、数字或者标点符号'), code='content')
        return password

