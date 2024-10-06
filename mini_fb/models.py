from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'