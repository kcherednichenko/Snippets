from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code', 'is_public']
        labels = {'name': '', 'lang': '', 'code': ''}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Snippet name'}),
            'code': Textarea(attrs={'placeholder': 'Snippet code'})
        }
