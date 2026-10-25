from django import forms
from .models import Comment, Post, Category

from django.contrib.postgres.search import SearchVectorField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': '1',
                'placeholder': 'leave a comment...',
                'class': (
                    'font-geist w-full bg-slate-900/50 text-slate-200 placeholder-slate-400 '
                    'text-sm rounded-xl px-4 py-2.5 border border-slate-700/60 '
                    'focus:outline-none focus:border-slate-500 transition-colors duration-300 '
                    'resize-none overflow-hidden block'
                ),
                'oninput': 'this.style.height = "auto"; this.style.height = (this.scrollHeight) + "px";',
            })
        }

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