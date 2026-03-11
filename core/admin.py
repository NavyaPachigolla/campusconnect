from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Branch, Subject, Doubt, Answer


# ✅ Custom User Admin (to show user_type)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('user_type',)}),
    )
    list_display = ('username', 'email', 'user_type', 'is_staff')


# ✅ Register Models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Doubt)
admin.site.register(Answer)