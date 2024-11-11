from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(choices=[('', 'All')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()], required=False)
    min_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False)
    max_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False)
    voter_score = forms.ChoiceField(choices=[('', 'All')] + [(score, score) for score in Voter.objects.values_list('voter_score', flat=True).distinct()], required=False)
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)