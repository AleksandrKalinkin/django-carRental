from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User
from django import forms

class UserLoginForm(AuthenticationForm): #создаем дочерний класс

    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': True}))

    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))

    class Meta: #Дочерний класс Meta- в качестве базовой модели будет использоваться user из user/models
        model = User
        fields = ('username', 'password') #нам нужны только эти поля при авторизации, а год рождения и тд - не нужно


class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': True}))

    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'required': True}))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79XXXXXXXXX', 'required': True}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))

    birth_day = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'required': True}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = User
        fields = ('username','email','phone_number','first_name', 'last_name','birth_day', 'password1', 'password2')

