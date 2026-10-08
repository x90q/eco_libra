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

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(email = data).exists():
            raise forms.ValidationError('this email is already in use')
        return data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        data = self.cleaned_data.get('email')
        query_set = User.objects.exclude(
            id = self.instance.id
        ).filter(
            email = data
        )

        if query_set.exists():
            raise forms.ValidationError('this email is already in use')

        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }