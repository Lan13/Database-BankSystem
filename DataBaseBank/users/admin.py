from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import BankUser


class BankUserInline(admin.StackedInline):
    model = BankUser
    can_delete = False
    verbose_name_plural = 'BankUser'


class BankUserAdmin(BaseUserAdmin):
    inlines = (BankUserInline,)


admin.site.unregister(User)
admin.site.register(User, BankUserAdmin)
# admin.site.register(BankUser)
