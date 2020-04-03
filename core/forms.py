from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.models import Subcategory, Post


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


class TagsListForm(forms.Form):
    tags = forms.MultipleChoiceField(choices=[])

    def set_tags_choices(self, subcategory_name):
        related_tags = Subcategory.objects.get(name=subcategory_name).tags.all()
        self.fields['tags'].choices = [(tag, tag) for tag in related_tags]


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
