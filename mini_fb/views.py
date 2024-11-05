from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
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
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_picture']
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            if 'user_form' not in context:
                context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            user_form = UserCreationForm(self.request.POST)
            if user_form.is_valid():
                user = user_form.save()
                form.instance.user = user
                return super().form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # Use the newly created profile's pk
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    fields = ['message', 'profile']
    template_name = 'mini_fb/create_status.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return form
  
    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        '''Attach the profile to the status message and handle file uploads'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        
        sm = form.save()
        files = self.request.FILES.getlist('files')
        
        for file in files:
            Image.objects.create(status_message=sm, image_file=file)
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_picture']
    template_name = 'mini_fb/update_profile.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status.html'
    success_url = '/'
    
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
    

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)