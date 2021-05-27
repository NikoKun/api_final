from django.db import models
from django.db.models import CASCADE

# Create your models here.
from django.contrib.auth.models import User


class UserInfo(models.Model):
    id_user = models.ForeignKey(User, on_delete=CASCADE)
    img = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    birthdate = models.DateTimeField(auto_now=True, auto_now_add=False)
    verified =  models.BooleanField(default=False)
    public =  models.BooleanField(default=False)
    token =  models.CharField(max_length=500)



class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=CASCADE, related_name='writer')
    in_response = models.ForeignKey(User, on_delete=CASCADE, related_name='in_response')
    body = models.CharField(max_length=500)
    images = models.CharField(max_length=500)
    publish_date = models.DateTimeField(auto_now=True, auto_now_add=False)



class Like(models.Model):
    id_post = models.ForeignKey(Post, on_delete=CASCADE)
    id_user = models.ForeignKey(User, on_delete=CASCADE)



class Follow(models.Model):
    id_user_followed = models.ForeignKey(User, on_delete=CASCADE, related_name='id_user_followed')
    id_user_folloing = models.ForeignKey(User, on_delete=CASCADE, related_name='id_user_folloing')
    notifications =  models.BooleanField(default=False)
    aproved =  models.BooleanField(default=True)








