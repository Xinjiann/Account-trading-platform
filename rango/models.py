from operator import mod
from re import T
from unicodedata import category
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Page(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class GameAccount(models.Model):
    accountName = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=128,unique=False)
    description = models.CharField(max_length=128,unique=False)
    category = models.CharField(max_length=128,unique=False,default='')
    price = models.IntegerField(default=0)
    seller = models.CharField(max_length=128,unique=False,default='')
    status = models.CharField(max_length=128,unique=False,default='onSale')

    def __str__(self):
        return self.accountName


class Order(models.Model):
    accountName = models.CharField(max_length=128,unique=True)
    buyer = models.CharField(max_length=128,unique=False,default='')
    date = models.CharField(max_length=128,unique=False)

    def __str__(self):
        return self.accountName
