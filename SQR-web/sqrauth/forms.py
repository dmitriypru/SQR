from qruser.models import User
from django import forms
from django.core.validators import RegexValidator

class UserRegisterForm(forms.Form):

    schools = (('1', 'МБОУ СОШ №45'), ('2', 'МБОУ лицей №4'))
    username = forms.CharField(label="Логин", max_length=25, widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    email = forms.CharField(label="Почта", max_length=25, widget=forms.EmailInput(attrs={'class': 'validate'}), required=True)
    password = forms.CharField(label="Пароль", max_length=25, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}), required=True)
    repass = forms.CharField(label="Подтверждение", max_length=25, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'confirm_password', 'onchange': 'checkPass ()'}), required=True)
    school = forms.ChoiceField(label="Школа", widget=forms.Select(attrs={'class': 'validate'}), choices=schools, required=True)
    klass = forms.CharField(label="Класс", max_length=4, widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    first_name = forms.CharField(max_length=25, required=True, validators=[RegexValidator(regex='^[а-яА-ЯёЁ]+$', message='Введите корректное имя', code='invalid_first_name'),], widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=25, required=True, validators=[RegexValidator(regex='^[а-яА-ЯёЁ]+$', message='Введите корректную фамилию', code='invalid_last_name'), ], widget=forms.TextInput(attrs={'id': 'last_name'}))

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('(Уже используется)')
        return email

class UserAuthForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", max_length=25,
                               widget=forms.PasswordInput(), required=True)
    class Meta:
        model = User
        fields = ['username', 'password']