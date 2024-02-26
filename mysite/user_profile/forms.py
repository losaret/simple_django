from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, CharField, EmailField, PasswordInput

class RegistrationForm(UserCreationForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control m-2'}))
    email = EmailField(widget=TextInput(attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control m-2'}))
    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2', }
        widgets = {
            'password1': PasswordInput(attrs={
                'class': "form-control"
            })
        }

