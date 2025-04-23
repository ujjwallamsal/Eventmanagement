from django import forms
from .models import Event, Contact, Post

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'time', 'recurrence']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text']
        widgets = {
            'post_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'}),
        }
