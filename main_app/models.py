from django.db import models

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=100)
    opensea_url = models.CharField(max_length=10000)
    banner_url = models.CharField(max_length=10000)
    num_editors = models.IntegerField()
    num_traits = models.IntegerField()
    created_date = models.DateField()
    total_sales = models.IntegerField()
    num_nfts = models.IntegerField()
    num_owners = models.IntegerField()
    average_price = models.DecimalField(max_digits=100, decimal_places=2)
    seven_day_sales = models.IntegerField()
    has_discord = models.BooleanField()
    has_twitter = models.BooleanField()
    has_instagram = models.BooleanField()
    has_wiki = models.BooleanField()
    description_words = models.IntegerField()
    cluster = models.CharField(max_length=100)     

