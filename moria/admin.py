from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'date_of_birth', 'phone_number', 'date_of_registration')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('date_of_birth', 'date_of_registration')

    # Fields to display when editing a profile
    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'date_of_birth', 'phone_number', 'date_of_registration')
        }),
    )
    readonly_fields = ('date_of_registration',)

    # Inline editing for User model fields like email and password
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj:
            return inlines
        return []