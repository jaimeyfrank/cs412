import sqlite3
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')
django.setup()

from project.models import Movie, Actor, Director

# Connect to the SQLite database
conn = sqlite3.connect('movie.sqlite')
cursor = conn.cursor()
print("huh")
# Load Movies
cursor.execute("SELECT id, name, year FROM Movie")
movies = cursor.fetchall()
for movie in movies:
    movie_id, title, year = movie
    Movie.objects.create(id=movie_id, title=title, year=year)

# Load Directors
cursor.execute("SELECT director_id, movie_id FROM Director")
directors = cursor.fetchall()
for director in directors:
    director_id, movie_id = director
    person = cursor.execute("SELECT id, name FROM Person WHERE id=?", (director_id,)).fetchone()
    if person:
        person_id, name = person
        director_obj, created = Director.objects.get_or_create(id=person_id, name=name)
        movie_obj = Movie.objects.get(id=movie_id)
        movie_obj.director.add(director_obj)

# Load Actors
cursor.execute("SELECT actor_id, movie_id FROM Actor")
actors = cursor.fetchall()
for actor in actors:
    actor_id, movie_id = actor
    person = cursor.execute("SELECT id, name FROM Person WHERE id=?", (actor_id,)).fetchone()
    if person:
        person_id, name = person
        actor_obj, created = Actor.objects.get_or_create(id=person_id, name=name)
        movie_obj = Movie.objects.get(id=movie_id)
        movie_obj.actors.add(actor_obj)

# Close the connection
conn.close()