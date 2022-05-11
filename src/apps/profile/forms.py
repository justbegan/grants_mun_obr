from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('middle_name', 'email', 'work_phone', 'phone', 'directions', 'education', 'locality', 'sex', 'organization', 'social')
        widgets = {
            'organization': forms.Textarea(attrs={'rows': 2}),
            'email': forms.EmailInput(),
            'work_phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
            'locality': forms.TextInput(attrs={'required': 'required', 'autocomplete': 'off', 'class': 'form-control'})
        }

