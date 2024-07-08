from django.contrib import admin
from users.models import CustomUser, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0

def is_verified(obj):
    return obj.profile.is_verified

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', is_verified]
    list_display_links = ['id', '__str__']
    search_fields = ['email']
    inlines = [ProfileInline]