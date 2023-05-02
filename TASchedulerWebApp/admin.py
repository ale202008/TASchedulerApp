from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserCreationForm, UserEditForm


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_confirm', 'first_name', 'last_name')}
        ),
    )
    add_form = UserCreationForm, UserEditForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Skill)
admin.site.register(Notification)
