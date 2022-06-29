from django.contrib.auth.models import Group
from django.contrib import admin
from .models import User, UserProfile, WatchList
# Register your models here.

# unregister group
admin.site.unregister(Group)

class Useradmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'username' )


admin.site.register(User, Useradmin)
admin.site.register(UserProfile)
admin.site.register(WatchList)