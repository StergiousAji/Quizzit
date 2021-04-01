from django import forms
from quizzit_app.models import UserProfile, Record
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
    
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('user', 'quiz', 'score')
