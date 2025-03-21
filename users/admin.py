from django.contrib import admin
from .models import CardioUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(CardioUser, UserAdmin)
