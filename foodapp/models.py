from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields.related import ForeignKey
import datetime

class userdata(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username

class restaurant(models.Model):
    name=models.CharField(max_length=100)
    rimg=models.ImageField(null=False, blank=True,upload_to='Rimages/')
    ratings=models.IntegerField()
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name

class items(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(null=False, blank=True,upload_to='Restos/')
    rest = models.ForeignKey(restaurant,on_delete=models.DO_NOTHING)
    item_price = models.IntegerField()
    duration = models.IntegerField()
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name


class cart(models.Model):
    user_name=models.ForeignKey(userdata,on_delete=models.DO_NOTHING)
    item=models.ForeignKey(items,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField()
    time=models.IntegerField()
    price=models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.user_name,self.item.name)
    

class orders(models.Model):
    user=models.ForeignKey(userdata,on_delete=models.DO_NOTHING)
    items=models.TextField()
    rest=models.ForeignKey(restaurant,on_delete=models.DO_NOTHING)
    total=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    local=models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.user,self.date)

class locality(models.Model):
    rest=models.ForeignKey(restaurant,on_delete=models.DO_NOTHING)
    keshwapur=models.IntegerField()
    Vidyanagar=models.IntegerField()
    Akshaypark=models.IntegerField()
    OldHubli=models.IntegerField()
    Hosur=models.IntegerField()

    def __str__(self):
        return self.rest.name
