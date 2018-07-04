from django.db import models
from django.contrib.auth.models import User
from campgrounds.models import Campground

# Create your models here.

class Comment(models.Model):
    """Comment model for campground """
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    campground = models.ForeignKey(Campground, related_name='comments', on_delete=models.CASCADE)
    