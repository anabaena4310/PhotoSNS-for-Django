from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    interests = models.ManyToManyField('Interest', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class Interest(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    caption = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

