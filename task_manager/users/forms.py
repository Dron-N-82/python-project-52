from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.contrib.auth.views import LoginView, LogoutView
# from django.forms import ModelForm
from .models import User
from django.utils.translation import gettext as _


# class CreateUserForm(forms.ModelForm):
class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        label=_("Password"), # 'Пароль'
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                }),
        # help_text=_('Your password must contain at least 3 characters.')
        help_text=f"<ul><li>{_('Your password must contain at least 3 characters.')}</li></ul>"
        # '<ul><li>Ваш пароль должен содержать как минимум 3 символа.</li></ul>'
        )
    
    # password_confirm = forms.CharField(
    password2 = forms.CharField(
        required=True,
        label=_("Confirm Password"), # 'Подтверждение пароля'
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                }),
        help_text=_('To confirm, please enter your password again.')
        # Для подтверждения введите, пожалуйста, пароль ещё раз.
        )
        
    
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                #   'password',
                #   'password_confirm'
                'password1',
                'password2',
                  ]
        labels = {
            'first_name': _('First name'),               # ваше кастомное имя для поля 'first_name' 'Имя'
            'last_name': _('Last_name'),                 # для 'last_name' 'Фамилия'
            'username': _('Username'),                   # для 'username' 'Имя пользователя'
        }
        help_texts = {
            'username': _('Required field. No more than 30 characters. Only letters, numbers, and symbols @/./+/-/_.')
            # Обязательное поле. Не более 30 символов. Только буквы, цифры и символы @/./+/-/_.
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
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(_("The passwords do not match."))
            # Пароли не совпадают.
            
            if len(password1) < 3:
                raise ValidationError(_("Password must be more than 3 characters."))
            # "Пароль должен быть болше 3-х символов."
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class LoginUserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': True
                }),
        label=_('Username'), # 'Имя пользователя'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                }),
        label=_("Password"), # 'Пароль'
        )
