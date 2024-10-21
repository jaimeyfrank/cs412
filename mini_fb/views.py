from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from typing import Any

from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *

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

class CreateProfileView(CreateView):
    '''the view to create a profile'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
       # Use the newly created profile's pk
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    '''the view to create a status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        '''Attach the profile to the status message and handle file uploads'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        
        # Save the status message to the database
        sm = form.save()
        
        # Read the files from the form
        files = self.request.FILES.getlist('files')
        
        # Create an Image object for each file
        for file in files:
            Image.objects.create(status_message=sm, image_file=file)
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})