from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat your password'
        })

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter your password'}
        ),
        help_text=(
            'Password must have at least one uppercase letter,'
            ' and at least one lowercase letter'
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat your password'}
        ),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Type your first name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Type your last name'}
            ),
        }
