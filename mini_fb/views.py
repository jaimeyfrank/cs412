from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from typing import Any

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
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
    
class UpdateProfileView(UpdateView):
    '''the view to update a profile'''
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
    '''the view to delete a status message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(UpdateView):
    '''the view to update a status message'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    
    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the status message to the context data'''
        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'