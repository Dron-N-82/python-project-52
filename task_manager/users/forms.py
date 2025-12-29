from django import forms
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# from django.forms import ModelForm
from .models import User


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                }),
        help_text='<ul><li>Ваш пароль должен содержать как минимум 3 символа.</li></ul>'
        )
    
    password_confirm = forms.CharField(
        required=True,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                }),
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
        )
        
    
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password',
                  'password_confirm'
                  ]
        labels = {
            'first_name': 'Имя',                 # ваше кастомное имя для поля 'first_name'
            'last_name': 'Фамилия',              # для 'last_name'
            'username': 'Имя пользователя',      # для 'username'
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 30 символов. Только буквы, цифры и символы @/./+/-/_.'
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                    'required': True}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                    'required': True}),
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                    'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError("Пароли не совпадают.")
            
            if len(password) < 3:
                raise ValidationError("Пароль должен быть болше 3-х символов.")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class LoginUserForm(forms.ModelForm):
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control',
    #             }),
    #     label='Пароль'
    #     )
    
    
    class Meta:
        model = User
        fields = ['username',
                  'password',
                  ]
        labels = {
            'username': 'Имя пользователя',      # для 'username'
            'password': 'Пароль'
            }
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                    'required': True}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control',
                    }),
            }