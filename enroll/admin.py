from django.contrib import admin
from .models import Profile
# Register your models here.
class AdminForm(admin.ModelAdmin):
   list_display=['mobile' , 'otp']

admin.site.register(Profile, AdminForm)   