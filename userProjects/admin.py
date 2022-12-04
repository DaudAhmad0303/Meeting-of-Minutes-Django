from django.contrib import admin
from .models import userProject,userProjectRecording

# Register your models here.

class userProjectsAdminPanel(admin.ModelAdmin):
    list_display=("projectName","creationDate",)
    list_filter=("projectName","creationDate",)
    
    
class userProjectRecordingsAdminPanel(admin.ModelAdmin):
    list_display=("folderName","fileName",)
    list_filter=("fileName","associatedProject__projectName",)

admin.site.register(userProject,userProjectsAdminPanel)
admin.site.register(userProjectRecording,userProjectRecordingsAdminPanel)