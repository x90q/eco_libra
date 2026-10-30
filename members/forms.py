from django import forms
from .models import Follow

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = []