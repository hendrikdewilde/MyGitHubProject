from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label=u'GitHub Username', required=True)
    password = forms.CharField(label=u'GitHub Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': 'autofocus',
            'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'autofocus': 'autofocus',
            'placeholder': 'Password'})
