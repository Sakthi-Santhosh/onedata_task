# permissions.py
from rest_framework.permissions import BasePermission
from .models import Role

def permission_validation(request):

    permission_data = {}

    permission_data['is_super_admin'] = request.user.roles.filter(name='Super Admin').exists()
    permission_data['is_admin'] = request.user.roles.filter(name='Admin').exists()
    permission_data['is_manager'] = request.user.roles.filter(name='Manager').exists()
    permission_data['is_member'] = request.user.roles.filter(name='Member').exists()

    return permission_data
