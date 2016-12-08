from django import forms

class NameForm(forms.Form):
    message = forms.Textarea(label='Сообщение')