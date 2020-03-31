from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=250, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=300, required=False, label='Имя')
    last_name = forms.CharField(max_length=300, required=False, label='Фамилия')
    email = forms.EmailField(required=False, label='Email')
    image = forms.ImageField(allow_empty_file=True, required=False)

