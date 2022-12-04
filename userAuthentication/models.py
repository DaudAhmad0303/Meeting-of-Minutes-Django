from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class user(models.Model):
    userID=models.IntegerField(default=1)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    userEmail=models.CharField(max_length=200,primary_key=True,db_index=True)
    userPassword=models.CharField(max_length=100,validators=[MinLengthValidator(8)])
    organizationName=models.CharField(max_length=100,default="None")
    contactNumber=models.CharField(max_length=50,default="None")
    activationStatus=models.BooleanField(default=False)
