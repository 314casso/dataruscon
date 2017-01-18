from django import forms
from emptystock.models import Sms

class SmsForm(forms.ModelForm):
    class Meta:
        model = Sms
        exclude = ['data','status',]