from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'password',
        widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'repeat password',
        widget = forms.PasswordInput
    )
    

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('passwords don\'t match')
        return cd.get('password2')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }