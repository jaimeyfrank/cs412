# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('onboarding/', views.OnboardingView.as_view(), name='onboarding'),
    path('recommendations/', views.RecommendationsView.as_view(), name='recommendations'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('user_data/', views.UserDataView.as_view(), name='user_data'),
]