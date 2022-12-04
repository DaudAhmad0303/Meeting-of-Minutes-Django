from django.db import models
from userAuthentication.models import user
from datetime import datetime

# Create your models here.

class userProject(models.Model):
    projectName=models.CharField(max_length=200)
    creationDate=models.DateTimeField(default=datetime.now())
    projectCreator=models.ForeignKey(user,on_delete=models.CASCADE,related_name="myProjects")
    
def getFilePath(instance,fileName):
    return f"{instance.associatedProject.projectCreator.userEmail}/{instance.folderName}/{fileName}"

class userProjectRecording(models.Model):
    myRecording=models.FileField(upload_to=getFilePath)
    folderName=models.CharField(max_length=200)
    fileName=models.CharField(max_length=200)
    associatedProject=models.ForeignKey(userProject,on_delete=models.CASCADE,related_name="associatedRecording")
    #display method overriden
    def __str__(self):
        return f"Name: {self.folderName}, Path: {self.myRecording}"