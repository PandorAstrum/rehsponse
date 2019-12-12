from django.contrib import admin
from rehsponse import models


# Register your models here.

@admin.register(models.UserProfile)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ["__str__", "created_on", "first_name", "last_name", "is_superuser", "is_staff"]


# @admin.register(models.UserProfile)
# class ProfileAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.Rehsponse)
class RehsponseAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ["__str__", "updated_on", "user_profile", "created_on"]


@admin.register(models.HashTag)
class HashTagAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ["__str__", "created_on"]


admin.site.site_header = "Rehsponse Administration"
