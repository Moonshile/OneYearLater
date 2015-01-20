
from django import forms
from forever import const

class HandInAnswerForm(forms.Form):
    id = forms.IntegerField()
    time = forms.IntegerField()
    q_token = forms.CharField()

    def __init__(self, post, op_ans, qids):
        forms.Form.__init__(self, post)
        self.op_ans = op_ans
        self.qids = qids

    def clean_id(self):
        id = self.cleaned_data['id']
        if id in self.op_ans and self.op_ans[id]['qid'] in self.qids:
            return id
        raise forms.ValidationError('id')

    def clean_time(self):
        time = self.cleaned_data['time']
        if time >= 0:
            return time
        raise forms.ValidationError('time')

    def clean_q_token(self):
        q_token = self.cleaned_data['q_token']
        id = self.cleaned_data.get('id', None)
        if id and self.qids[self.op_ans[id]['qid']][0] == q_token:
            return q_token
        raise forms.ValidationError('q_token')

class FinishAnswerForm(forms.Form):
    q_token = forms.CharField()

    def __init__(self, post, session):
        forms.Form.__init__(self, post)
        self.session = session

    def clean_q_token(self):
        q_token = self.cleaned_data['q_token']
        if self.session.get(q_token, None) == 0:
            return q_token
        raise forms.ValidationError('q_token')
