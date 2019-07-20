from django import forms
from django.contrib.auth.models import User
from .models import Book, Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender']


class BookForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    class Meta:
        model = Book
        fields = ['name', 'author', 'isbn', 'publish_on', 'picture', 'about']
        widgets = {
            'publish_on': forms.DateTimeInput(attrs={'type': 'date'})
        }
        

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label='Full Name')
    email = forms.EmailField(required=True)
    body = forms.CharField(widget=forms.Textarea, help_text='write your message here')

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == 'ahmed':
            raise forms.ValidationError('ommm, sorry you cann\' send us message')

        return name

