from django import forms
from .models import Message,Comment

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['content','photo']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'photo':forms.FileInput(attrs={'class':'form-control-file'}),
        }
        labels={
            'content':'投稿内容',
            'photo':'',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content',]
        widgets={
            'content':forms.Textarea(attrs={
                'class':'form-control',
                'rows':2,
                'placeholder':'何を考えていますか？',
            }),
        }
        labels={
            'content':'コメント',
        }