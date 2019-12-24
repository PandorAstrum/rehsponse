from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Rehsponse, UserProfile
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class RehsponseModelForm(forms.ModelForm):
    """A form for posting response"""
    rehsponse_text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'your response', 'class': 'form-control'}))

    class Meta:
        model = Rehsponse
        fields = [
            "rehsponse_text"
        ]


class RegistrationModelForm(forms.Form):
    """A form for sign up"""
    user_name = forms.CharField(label="Username:", widget=forms.TextInput(attrs={'placeholder': 'Choose a username'}))
    first_name = forms.CharField(label="First Name:", widget=forms.TextInput(attrs={'placeholder': 'Your first name'}))
    last_name = forms.CharField(label="Last Name:", widget=forms.TextInput(attrs={'placeholder': 'Your last name'}))
    email = forms.CharField(label="Email:", widget=forms.EmailInput(attrs={'placeholder': 'Enter a valid email'}))
    password = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(user_name__icontains=user_name).exists():
            raise forms.ValidationError("This user name is taken")
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email


class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'short_bio',
            'address',
            'city',
            'country',
            'phone',
            'date_of_birth'
        ]


class UserProfileCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'user_name', 'password')


class UserProfileChangeForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'user_name')
