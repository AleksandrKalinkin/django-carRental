from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'birth_day')
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. поля', {'fields': ('phone_number', 'birth_day')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Доп. поля', {'fields': ('phone_number', 'birth_day')}),
    )

admin.site.register(User, CustomUserAdmin)
