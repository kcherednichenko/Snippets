from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, CharField, PasswordInput
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


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")

        if pass1 and pass2 and pass1 == pass2:
            return pass2

        raise ValidationError("Passwords don't match or they are empty")

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
