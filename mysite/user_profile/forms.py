from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model, password_validation
from .models import ExtendUser


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "E-mail",
            }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Имя",
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Фамилия",
            }),
        }

class ExtendUserForm(forms.ModelForm):
    class Meta:
        model = ExtendUser
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
            'class': 'form-control',
        }),
        }


class RegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "password_mismatch": _("Пароль не совпадают."),
    }
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': "form-select m-2",
            "style": "width: 300px;"            
        }),
        help_text=_("Пароль должен содержать более 8 символов и не быть полностью из чисел"),
    )
    password2 = forms.CharField(
        label=_("Подтвердите пароль"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': "form-select m-2",
            "style": "width: 300px;"
        }),
        strip=False,
        help_text=_("Введите тот же пароль для верификации"),
    )

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Логин",
                "style": "width: 300px;"
            }),
            'email': forms.TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Почта",
                "style": "width: 300px;"
            }),
        }

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


