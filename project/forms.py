# forms.py
from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['movie', 'rating']

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name']

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name']

class OnboardingForm(forms.Form):
    liked_actors = forms.ModelMultipleChoiceField(queryset=Actor.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    liked_directors = forms.ModelMultipleChoiceField(queryset=Director.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    ratings = forms.CharField(widget=forms.HiddenInput(), required=False)  # Store ratings as JSON