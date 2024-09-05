import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attribute(field, attr_name, attr_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_value}'.strip()


def add_placeholder(field, value):
    add_attribute(field, 'placeholder', value)


def clean_password(self):
    cleaned_data = super().clean()

    password = cleaned_data.get('password')
    password2 = cleaned_data.get('password2')

    if password != password2:
        match_error = ValidationError(
            'Passwords do not match',
            code='invalid',
        )

        raise ValidationError({
            'password': match_error,
            'password2': match_error,
        })


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Password is not strong enough'
                # 'Password must have at least one uppercase letter,'
                # ' and at least one lowercase letter'
            ),
            code='invalid',
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add_placeholder(self.fields['email'], 'Enter your email')

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Ex.: John',
        })

    username = forms.CharField(
        label='Utilizador',
        required=True,
        min_length=5,
        max_length=150,
        error_messages={
            'required': 'Username is required',
            'min_length': 'Username must be at least 5 characters',
            'max_length': 'Username must not exceed 150 characters',
        },
        help_text=(
            'Required. At least 5 characters. '
            'Only letters, digits and @.-_ are allowed'
        ),
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={'required': 'Email is required'},
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter your password'}
        ),
        error_messages={'required': 'Password must be informed'},
        help_text=(
            'Password must have at least one uppercase letter,'
            ' and at least one lowercase letter'
        ),
        validators=[strong_password],
    )
    password2 = forms.CharField(
        label='Repeat Password',
        required=True,
        error_messages={'required': 'Repeat your password'},
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat your password'}
        ),
        validators=[strong_password],
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
            'last_name': forms.TextInput(attrs={'placeholder': 'Ex.: Doe'}),
        }
