from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=3000)
    gender = models.CharField(max_length=300)


class early_detection_of_human_diseases(models.Model):

    Fid= models.CharField(max_length=300)
    Age= models.CharField(max_length=300)
    Sex= models.CharField(max_length=300)
    Bmi= models.CharField(max_length=300)
    Fbg= models.CharField(max_length=300)
    hbA1c= models.CharField(max_length=300)
    Bps= models.CharField(max_length=300)
    Bpd= models.CharField(max_length=300)
    Ct= models.CharField(max_length=300)
    Ggt= models.CharField(max_length=300)
    Su= models.CharField(max_length=300)
    Pal= models.CharField(max_length=300)
    Dic= models.CharField(max_length=300)
    Ac= models.CharField(max_length=300)
    Ss= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)

class early_detection_of_human_diseases1(models.Model):

    Fid= models.CharField(max_length=300)
    Age= models.CharField(max_length=300)
    Sex= models.CharField(max_length=300)
    Bmi= models.CharField(max_length=300)
    Fbg= models.CharField(max_length=300)
    hbA1c= models.CharField(max_length=300)
    Bps= models.CharField(max_length=300)
    Bpd= models.CharField(max_length=300)
    Ct= models.CharField(max_length=300)
    Ggt= models.CharField(max_length=300)
    Su= models.CharField(max_length=300)
    Pal= models.CharField(max_length=300)
    Dic= models.CharField(max_length=300)
    Ac= models.CharField(max_length=300)
    Ss= models.CharField(max_length=300)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



