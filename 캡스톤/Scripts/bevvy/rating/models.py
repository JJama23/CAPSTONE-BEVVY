from django.db import models
from django.core.validators import URLValidator

# Create your models here.
class Beer(models.Model):
    beer_id = models.AutoField(primary_key=True)
    beer_name = models.CharField(max_length=45, blank=True, null=True)
    candidate = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        # managed = False
        db_table = 'rating_beer'


class RatingBeer(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rate = models.FloatField()
    user_id = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=50, blank=True, null=True)
    beer_id = models.IntegerField(blank=True, null=True)
    tap = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'rating_ratingbeer'


class RateBeer(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rate = models.FloatField()
    user_id = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=50, blank=True, null=True)
    beer_id = models.ForeignKey(Beer,on_delete=models.CASCADE)
