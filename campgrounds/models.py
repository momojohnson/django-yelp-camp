from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Max, Min, Sum, Avg

def validate_price(value):
    """ Validate price to ensure that price is greater than zero"""
    if value  <= 0:
        raise ValidationError(
            _('%(value)s is not a valid price. Price must be greater than zero.'),
            params={'value': value},
        )
class Campground(models.Model):
    """ Model for Yelp Campground """
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200)
    lat = models.IntegerField(null=True)
    lng = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_price])
    location = models.CharField(max_length=250)
    description = models.TextField()
    image_id = models.CharField(max_length=250, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='campgrounds', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Campground, self).save(*args, **kwargs)
            
    
    def get_total_campgrounds(self):
        return Campground.objects.count()
    
    def get_total_number_of_current_user(self):
        return User.objects.count()
    
    def get_max_and_min_campground_price(self):
        return Campground.objects.aggregate(Avg('price'), Max('price'), Min('price'))