# views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.db.models import Avg

from .models import *
from .forms import *
from .util import auto_likes

class HomeView(View):
    def get(self, request):
        return render(request, 'project/home.html')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'project/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            request.session['profile_id'] = profile.id
            return redirect('onboarding')
        return render(request, 'project/signup.html', {'form': form})
    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'project/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                profile = Profile.objects.get(user=user)
                request.session['profile_id'] = profile.id
                return redirect('home')
        return render(request, 'project/login.html', {'form': form, 'error': 'Invalid email or password'})


class LogoutView(View):
    def get(self, request):
        if 'profile_id' in request.session:
            del request.session['profile_id']
        return redirect('home')


class OnboardingView(View):
    def get(self, request):
        form = OnboardingForm()
        movies = Movie.objects.filter(year__gte=2020)[:25]
        actors = Actor.objects.filter(movies__in=movies).distinct()[:25]
        directors = Director.objects.filter(movies__in=movies).distinct()[:25]
        return render(request, 'project/onboarding.html', {
            'form': form,
            'movies': movies,
            'actors': actors,
            'directors': directors
        })
    
    def post(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return JsonResponse({'error': 'User not logged in'}, status=400)
        
        profile = Profile.objects.get(id=profile_id)
        form = OnboardingForm(request.POST)
        
        if form.is_valid():
            liked_actors = form.cleaned_data['liked_actors']
            liked_directors = form.cleaned_data['liked_directors']
            ratings = json.loads(form.cleaned_data['ratings'])
            
            profile.liked_actors.set(liked_actors)
            profile.liked_directors.set(liked_directors)
            
            for movie_id, rating_value in ratings.items():
                movie = Movie.objects.get(id=movie_id)
                Rating.objects.create(user=profile, movie=movie, rating=rating_value)
            
            auto_likes(profile)
            return redirect('recommendations')
        
        movies = Movie.objects.filter(year__gte=2020)
        actors = Actor.objects.filter(movies__in=movies).distinct()
        directors = Director.objects.filter(movies__in=movies).distinct()
        return render(request, 'project/onboarding.html', {
            'form': form,
            'movies': movies,
            'actors': actors,
            'directors': directors
        })


class RecommendationsView(View):
    def get(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('signup')
        
        profile = Profile.objects.get(id=profile_id)
        recommended_movies = profile.recommend_movies()
        return render(request, 'project/recommendations.html', {'recommended_movies': recommended_movies})

    def post(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return JsonResponse({'error': 'User not logged in'}, status=400)
        
        profile = Profile.objects.get(id=profile_id)
        auto_likes(profile)

        movie_id = request.POST.get('movie_id')
        want_to_watch = request.POST.get('want_to_watch')
        rating_value = request.POST.get('rating')
        
        movie = Movie.objects.get(id=movie_id)
        rating, created = Rating.objects.get_or_create(user=profile, movie=movie)
        
        if rating_value:
            rating.rating = rating_value
            rating.want_to_watch = False
            rating.save()
            return JsonResponse({'success': True, 'rated': True})
        
        if want_to_watch is not None:
            if want_to_watch == 'false':
                rating.delete()
                return JsonResponse({'success': True, 'deleted': True})
            else:
                rating.want_to_watch = True
                rating.save()
                return JsonResponse({'success': True, 'added': True})
        
        return JsonResponse({'error': 'Invalid request'}, status=400)


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        movies = []
        actors = []
        directors = []
        
        if query:
            movies = Movie.objects.filter(title__icontains=query)
            actors = Actor.objects.filter(name__icontains=query)
            directors = Director.objects.filter(name__icontains=query)
        
        return render(request, 'project/search.html', {
            'movies': movies,
            'actors': actors,
            'directors': directors
        })

    def post(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return JsonResponse({'error': 'User not logged in'}, status=400)
        
        profile = Profile.objects.get(id=profile_id)
        movie_id = request.POST.get('movie_id')
        actor_id = request.POST.get('actor_id')
        director_id = request.POST.get('director_id')
        want_to_watch = request.POST.get('want_to_watch')
        rating_value = request.POST.get('rating')
        
        if movie_id:
            movie = Movie.objects.get(id=movie_id)
            rating, created = Rating.objects.get_or_create(user=profile, movie=movie)
            
            if rating_value:
                rating.rating = rating_value
                rating.want_to_watch = False
                rating.save()
                return JsonResponse({'success': True, 'rated': True})
            
            if want_to_watch is not None:
                if want_to_watch == 'false':
                    rating.delete()
                    return JsonResponse({'success': True, 'deleted': True})
                else:
                    rating.want_to_watch = True
                    rating.save()
                    return JsonResponse({'success': True, 'added': True})
        
        if actor_id:
            actor = Actor.objects.get(id=actor_id)
            profile.liked_actors.add(actor)
            return JsonResponse({'success': True, 'liked_actor': True})
        
        if director_id:
            director = Director.objects.get(id=director_id)
            profile.liked_directors.add(director)
            return JsonResponse({'success': True, 'liked_director': True})
        
        return JsonResponse({'error': 'Invalid request'}, status=400)


class UserDataView(LoginRequiredMixin, View):
    def get(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('login')
        
        profile = Profile.objects.get(id=profile_id)
        rated_movies = Rating.objects.filter(user=profile, want_to_watch=False).exclude(rating__isnull=True).select_related('movie')
        liked_actors = profile.liked_actors.all()
        liked_directors = profile.liked_directors.all()
        watchlist = Rating.objects.filter(user=profile, want_to_watch=True).select_related('movie')
        
        return render(request, 'project/user_data.html', {
            'rated_movies': rated_movies,
            'liked_actors': liked_actors,
            'liked_directors': liked_directors,
            'watchlist': watchlist
        })

    def post(self, request):
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('login')
        
        profile = Profile.objects.get(id=profile_id)
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        remove = request.POST.get('remove')
        
        movie = Movie.objects.get(id=movie_id)
        rating, created = Rating.objects.get_or_create(user=profile, movie=movie)
        
        if remove:
            rating.want_to_watch = False
            if rating.rating is None:
                rating.delete()
            else:
                rating.save()
        elif rating_value:
            rating.rating = rating_value
            rating.want_to_watch = False
            rating.save()
        
        return redirect('user_data')