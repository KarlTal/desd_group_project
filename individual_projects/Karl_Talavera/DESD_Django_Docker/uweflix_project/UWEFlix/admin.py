from django.contrib import admin

# Register your models here.
from .models import Films,Accounts

admin.site.register(Films)
admin.site.register(Accounts)
