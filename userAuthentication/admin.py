from django.contrib import admin
from .models import user

# Register your models here.

class userAdminPannel(admin.ModelAdmin):
    list_display=("firstName","lastName","userEmail",)
    list_filter=("firstName","userEmail",)
    

admin.site.register(user,userAdminPannel)
