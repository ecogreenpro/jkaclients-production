from django.contrib import admin

from authentication.models import Profile, Team
from django.utils.translation import gettext as _


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_photo',
        '__str__',
        'is_active',
        'is_verify',
    ]
    fieldsets = (
        (_('Auth'), {'fields': ('user', 'client_id', 'image')}),
        (_('General Info'), {'fields': ('date_of_birth', 'gender', 'address', 'district')}),
        (_('Verification'), {'fields': ('phone', 'otp', 'is_verify')}),
        (_('Permission'), {'fields': ('is_company', 'is_active')}),
    )


admin.site.register(Profile, ProfileAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'job_title',
        'email',
        'phone',
    ]


admin.site.register(Team, TeamAdmin)
