from django import forms
from .models import Comment, Post, Category

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

class SlashModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"/{obj.name}"

class PostCreateForm(forms.ModelForm):
    category = SlashModelChoiceField(
    queryset=Category.objects.all()
    )
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']