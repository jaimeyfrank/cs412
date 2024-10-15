from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.

class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''the view to show the profile page'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'