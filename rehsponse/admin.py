from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rehsponse.forms import UserProfileCreationForm, UserProfileChangeForm
from rehsponse import models


@admin.register(models.Rehsponse)
class RehsponseAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ["__str__", "updated_on", "user_profile", "created_on"]


@admin.register(models.HashTag)
class HashTagAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ["__str__", "created_on"]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_active"]


class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm
    model = models.UserProfile
    date_hierarchy = "created_on"
    list_display = ["__str__", "created_on", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active"]
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'user_name')}),
        ('Extra Info', {'fields': ('user_image',
                                   'height_field',
                                   'width_field',
                                   'short_bio',
                                   'date_of_birth',
                                   'address',
                                   'city',
                                   'country',
                                   'phone')}),
        ('Useful Dates', {'fields': ('last_login',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.site_header = "Rehsponse Administration"
