from django import forms
from users   import models

class LoginForm(forms.Form):

    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(self.cleaned_data, )
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError('User Does Not Exist')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        print(password)
        return 'lalalalalalala'