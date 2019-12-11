from django import forms
from .models import Rehsponse


class RehsponseModelForm(forms.ModelForm):
    """A form for posting response"""
    rehsponse_text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'your response', 'class': 'form-control'}))

    class Meta:
        model = Rehsponse
        fields = [
            "rehsponse_text"
        ]
