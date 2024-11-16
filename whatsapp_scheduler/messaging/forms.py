from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['phone', 'message', 'send_time']
        widgets = {
            'send_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
