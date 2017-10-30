
from django import forms

from django_troll.models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', 'object_id', 'content_type']
        widgets = {
            'object_id': forms.HiddenInput,
            'content_type': forms.HiddenInput,
        }