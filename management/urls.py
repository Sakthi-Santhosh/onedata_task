from django.urls import path
from .views import *


urlpatterns = [
    path('login/',LoginView.as_view()),

    #Organization
    path('organization/',OrganizationView.as_view()),
    path('organization-list/',OrganizationListView.as_view()),

    #Role
    path('role/',RoleView.as_view()),
    path('role-list/',RoleListView.as_view()),

    #User
    path('user/',UserView.as_view()),
    path('user-list/',UserListView.as_view()),
    path('user-role/',RoleAssignView.as_view()),
]