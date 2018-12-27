from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=_("Username"),
        max_length=32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Username")}
        )
    )

    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Email")}
        )
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Password")}
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                _("Sorry, user with that username already exist.")
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Sorry, that email already exist."))
        return self.cleaned_data


class UserLoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Email")}
        )
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Password")}
        )
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(_("Incorrect password."))
            elif not user.is_active:
                raise forms.ValidationError(_("User with this e-mail is blocked."))
        except User.DoesNotExist:
            raise forms.ValidationError(_("User with this e-mail does not exist."))
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
        return user
