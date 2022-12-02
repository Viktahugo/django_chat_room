from django import forms
from chatApp.models import Message

class SaveMessage(forms.ModelForm):
    username = forms.CharField(max_length=250, help_text="Enter Username")
    message = forms.Textarea()

    class Meta:
        model = Message
        fields = ('username', 'message',)
