from django.conf import settings
from django.db import models
from django.db.models import Count, Q, F
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    rated_movies = models.ManyToManyField('Movie', through='Rating', related_name='rated_by')
    liked_actors = models.ManyToManyField('Actor', related_name='liked_by_users')
    liked_directors = models.ManyToManyField('Director', related_name='liked_by_users')

    def recommend_movies(self):
        """
        Recommends movies based on liked actors, directors, and user's ratings.
        Returns a list of top 25 recommended movies.
        """
        recommended_movies = (
            Movie.objects.annotate(
                actor_score=Count(
                    'actors',
                    filter=Q(actors__in=self.liked_actors.all())
                ) * 2,
                director_score=Count(
                    'director',
                    filter=Q(director__in=self.liked_directors.all())
                ) * 3,
                total_score=F('actor_score') + F('director_score'),
            )
            .exclude(rated_by=self)
            .order_by('-total_score')
        )

        return recommended_movies[:25]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Movie(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    actors = models.ManyToManyField('Actor', related_name='movies')
    director = models.ManyToManyField('Director', related_name='movies')

    def __str__(self):
        return f"{self.title} ({self.year})"

class Actor(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Director(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(blank=True, null=True)
    want_to_watch = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} rated {self.movie}: {self.rating}/5"