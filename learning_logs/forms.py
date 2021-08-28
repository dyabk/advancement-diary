from django import forms

from .models import Topic, Entry, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'public']
        labels = {'name': '', 'public': 'Create a public topic.'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}