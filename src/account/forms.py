from django import forms
from models import InvitationCode

import re

max_len_msg = u'不长于%d个字符'
min_len_msg = u'不短于%d个字符'

class SignUpForm(forms.Form):
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
    invitation_code = forms.CharField(error_messages={
        'invalid': u'是字母或者数字',
    })

    def clean_username(self):
        pattern = re.compile(u'^[a-zA-Z0-9_\u4e00-\u9fa5]+$')
        username = self.cleaned_data['username']
        if not pattern.match(username):
            raise forms.ValidationError(_(u'是字母、数字或者汉字'), code='username')
        return username

    def clean_password(self):
        pattern = re.compile(u'^[\x21-\x7e]+$')
        password = self.cleaned_data['password']
        if not pattern.match(password):
            raise forms.ValidationError(_(u'是半角字母、数字或者标点符号'), code='password')
        return password

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password = self.data['password']
        if password2 != password:
            raise forms.ValidationError(_(u'与第一次输入一致'), code='password2')
        return password2

    def clean_invitation_code(self):
        invitation_code = self.cleaned_data['invitation_code']
        if InvitationCode.objects.filter(code=invitation_code).count() == 0:
            raise forms.ValidationError(_(u'邀请码错误'), code='invitation_code')
        raise invitation_code

class SigninForm(forms.Form):
    username = forms.CharField(error_messages={
        'invalid': u'用户名或者邮箱',
    })
    password = forms.CharField(max_length=15, min_length=6, error_messages={
        'max_length': max_len_msg % 15,
        'min_length': min_len_msg % 6,
        'invalid': u'是半角字母、数字或者标点符号',
    })

    def clean_username(self):
        pattern = re.compile(u'^[a-zA-Z0-9_\u4e00-\u9fa5]+$')
        email = forms.EmailField()
        username = self.cleaned_data['username']
        if not pattern.match(username) or not email.clean(username):
            raise forms.ValidationError(_(u'是字母、数字或者汉字，或者你的邮箱'), code='username')
        return username

    def clean_password(self):
        pattern = re.compile(u'^[\x21-\x7e]+$')
        password = self.cleaned_data['password']
        if not pattern.match(password):
            raise forms.ValidationError(_(u'是半角字母、数字或者标点符号'), code='password')
        return password

