from django.db.models import Count, Q

def auto_likes(profile):
    """
    Automatically like actors and directors for a given profile based on liked movies.
    """
    # Find actors to like
    actors_to_like = (
        profile.rated_movies.values('actors__id')
        .annotate(liked_count=Count('id', filter=Q(rating__gte=4)))
        .filter(liked_count__gte=3)
    )
    profile.liked_actors.add(*[actor['actors__id'] for actor in actors_to_like])

    # Find directors to like
    directors_to_like = (
        profile.rated_movies.values('director__id')
        .annotate(liked_count=Count('id', filter=Q(rating__gte=4)))
        .filter(liked_count__gte=3)
    )
    profile.liked_directors.add(*[director['director__id'] for director in directors_to_like])