from django.contrib import admin

from .models import Organization, Role, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'password',
        'last_login',
        'id',
        'username',
        'email',
        'organization',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('last_login', 'organization', 'is_staff', 'is_superuser')
    raw_id_fields = ('roles',)