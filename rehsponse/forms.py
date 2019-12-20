from django import forms
from .models import Rehsponse, UserProfile


class RehsponseModelForm(forms.ModelForm):
    """A form for posting response"""
    rehsponse_text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'your response', 'class': 'form-control'}))

    class Meta:
        model = Rehsponse
        fields = [
            "rehsponse_text"
        ]


class UserModelForm(forms.ModelForm):
    """A form for updating"""
    username = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'your response', 'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = [
            "username",
            # "last_name",
            # "email",
            # "short_bio",
            # "address"
        ]
