from django.db import models


class Dannie(models.Model):
    url = models.CharField(max_length=255,unique=True)
    domain = models.TextField()
    create_date = models.TextField()
    update_date = models.TextField()
    country = models.TextField()
    isDead = models.TextField()
    A= models.TextField()
    NS = models.TextField()
    CNAME = models.TextField()
    MX = models.TextField()
    TXT = models.TextField()













