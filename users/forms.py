from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',

        }   
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input', 'id': 'formInput#text'})
        # self.fields['title'].widget.attrs.update({'class': 'input'})

    
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input', 'id': 'formInput#text'})


class skillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(skillForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input', 'id': 'formInput#text'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input', 'id': 'formInput#text'})