from django.db import models

# Create your models here.
class trainer(models.Model):
    tr_name =  models.CharField(max_length=20)
    tr_desc = models.TextField(max_length=100)
    tr_img = models.ImageField(upload_to="img")
    '''
class memberships(models.Model):
    name=models.CharField(max_length=20)
    val=models.CharField(max_length=20)
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
'''
    