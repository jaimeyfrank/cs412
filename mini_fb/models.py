from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_picture = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)
    
    def add_friend(self, other):
        if self == other:
            return
        
        if not Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists():
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        
        suggestions = Profile.objects.exclude(id__in=friend_ids).exclude(id=self.id)
        
        return suggestions
    
    def get_news_feed(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        
        profile_ids = friend_ids + [self.id]
        
        news_feed = StatusMessage.objects.filter(profile_id__in=profile_ids).order_by('-timestamp')
        
        return news_feed


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile} - {self.timestamp}'
    
    def get_images(self):
        return Image.objects.filter(status_message=self)
    

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.status_message} at {self.timestamp}'
    

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile1} & {self.profile2}'