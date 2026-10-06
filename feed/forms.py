from django import forms
from .models import Comment

from django.contrib.postgres.search import SearchVectorField

class EmailPostForm(forms.Form):
    to = forms.EmailField()
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
        max_length=500
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
