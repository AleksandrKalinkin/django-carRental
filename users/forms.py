from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms
from datetime import date
from django.core.exceptions import ValidationError

from TG_bot.main import user_states


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+79XXXXXXXXX',
            'required': True
        })
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    birth_day = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True,
            'max': str(date.today().replace(year=date.today().year - 21))  # Ограничение в HTML
        }),
        help_text="Для регистрации вам должно быть не менее 21 года"
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    agreement = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
        error_messages={
            'required': 'Необходимо дать согласие на обработку персональных данных'
        },
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'birth_day', 'password1', 'password2')

    def clean_birth_day(self):
        birth_day = self.cleaned_data['birth_day']
        today = date.today()
        age = today.year - birth_day.year - ((today.month, today.day) < (birth_day.month, birth_day.day))

        if age < 21:
            raise ValidationError("Для регистрации вам должно быть не менее 21 года")
        return birth_day

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:  # Проверяем только если номер указан
            if User.objects.filter(phone_number=phone_number).exists():
                raise forms.ValidationError("Этот номер телефона уже используется")
        return phone_number

class UserProfileForm(UserChangeForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True, 'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_day = forms.DateField(widget=forms.DateInput(attrs={'readonly': True, 'type': 'date','class': 'form-control'},format='%Y-%m-%d'))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number','birth_day', 'image')