from django import forms
from django.contrib.auth import get_user_model
from members.models import Profile

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }