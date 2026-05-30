from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

FIELD_CLASSES = 'w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 focus:ring-2 focus:ring-orange-500'


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': FIELD_CLASSES}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': FIELD_CLASSES}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': FIELD_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': FIELD_CLASSES}),
            'email': forms.EmailInput(attrs={'class': FIELD_CLASSES}),
        }
