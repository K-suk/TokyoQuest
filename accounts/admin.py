from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('account_id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'contact_address', 'level', 'done', 'due')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('account_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('account_id', 'email', 'first_name', 'last_name')
    ordering = ('account_id',)

admin.site.register(User, UserAdmin)
admin.site.register(Token, TokenAdmin)