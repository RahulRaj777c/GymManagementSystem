from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class trainer(models.Model):
    tr_name =  models.CharField(max_length=20)
    tr_desc = models.TextField(max_length=100)
    tr_img = models.ImageField(upload_to="img")
    
class memberships(models.Model):
    name=models.CharField(max_length=20)
    val=models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
class coaches(models.Model):
    name=models.CharField(max_length=50)
    desc=models.CharField(max_length=50)
    img=models.ImageField(upload_to="pic")
class coaches(models.Model):
    img=models.ImageField(upload_to="pic")
    name=models.CharField(max_length=20)

    age=models.IntegerField()
    desc=models.CharField(max_length=50)

class classes(models.Model):
    name=models.CharField(max_length=20)

class Attendance(models.Model):
    attendance=models.BooleanField(("false"))
class payment(models.Model):
    payment=models.BooleanField(("fasle"))

class TrainerProfile(models.Model):
    tr_name =  models.CharField(max_length=20)
    tr_desc = models.TextField(max_length=100)
    tr_img = models.ImageField(upload_to="img")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_trainer = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    User_name =  models.CharField(max_length=20)
    tr_desc = models.TextField(max_length=100)
    tr_img = models.ImageField(upload_to="img")

def user_directory_path(instance, filename):
    return f'user_{instance.id}/{filename}'
