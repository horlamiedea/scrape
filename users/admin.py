from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active',]
    list_filter = ['email', 'is_staff', 'is_active',]

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'date_joined')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')},
         ),
        ('Permissions', {'fields': ('is_active',)})
    )
    search_fields = ('email',)
    ordering = ('email',)

    # readonly_fields = ['wallet']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["email", 'date_joined', 'password',]
        else:
            return ['date_joined']