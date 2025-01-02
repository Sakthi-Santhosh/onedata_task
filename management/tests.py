from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from django.utils import timezone
from rest_framework.authtoken.models import Token

class ManagementTest(TestCase):

    def setUp(self):
        
        self.client = APIClient()

        self.organization = Organization.objects.create(name="One Data",description="One Data",created_at=timezone.now())

        roles = ["Super Admin","Admin","Manager","Member"] 

        self.role_instance = []

        for role in roles:

            role_queryset = Role.objects.create(name=role,description=role,organization=self.organization) 

            self.role_instance.append(role_queryset)    

        self.user, created = User.object.get_or_create(username='admin', password='12345',email='admin@example.com',organization=self.organization)

        self.user.roles.set(self.role_instance)

        self.super_admin_role_queryset = Role.objects.get(name="Super Admin")
        self.admin_role_queryset = Role.objects.get(name="Admin")
        self.manager_role_queryset = Role.objects.get(name="Manager")
        self.member_role_queryset = Role.objects.get(name="Member")


        
        self.token, created = Token.objects.get_or_create(user=self.user)
        
        self.organization_url = '/management/organization/'
        self.role_url = '/management/role/'
        
        self.header = {
            "Authorization": f"Token {self.token.key}",
            'Content-Type': 'application/json'
        }

    def test_create_organization(self):

        #user with all role
        
        organization_create_data = {
            "name": "Test Organization",
            "description": "This is a test organization."
        }

        response = self.client.post(self.organization_url, data=organization_create_data, headers=self.header, format='json')


        self.assertEqual(response.data['status'], status.HTTP_200_OK,"Expected status code 200 OK, but got {0}".format(response.data['status']))

    def test_super_admin_create_organization(self):

        super_admin_organization_create_data = {
            "name": "Super Admin Test Organization",
            "description": "This is a test organization by Super Admin."
        }

        #checks wether user with Super admin role alone create organization

        

        self.user.roles.set([self.super_admin_role_queryset])

        response = self.client.post(self.organization_url, data=super_admin_organization_create_data, headers=self.header, format='json')

        self.assertEqual(response.data['status'], status.HTTP_200_OK,"Expected status code 200 OK, but got {0}".format(response.data['status']))

    def test_admin_create_organization(self):

        admin_organization_create_data = {
            "name": "Admin Test Organization",
            "description": "This is a test organization by Admin."
        }

        #checks wether user with admin role alone create organization

        self.user.roles.set([self.admin_role_queryset])

        response = self.client.post(self.organization_url, data=admin_organization_create_data, headers=self.header, format='json')

        self.assertEqual(response.data['status'], status.HTTP_200_OK,"Expected status code 200 OK, but got {0}".format(response.data['status']))

    def test_manager_create_organization(self):

        manager_organization_create_data = {
            "name": "Manager Test Organization",
            "description": "This is a test organization by Manager."
        }

        #checks wether user with manager role alone create organization


        self.user.roles.set([self.manager_role_queryset])

        response = self.client.post(self.organization_url, data=manager_organization_create_data, headers=self.header, format='json')

        self.assertEqual(response.data['status'], status.HTTP_401_UNAUTHORIZED,"Expected status code 401 UNAUTHORIZED, but got {0}".format(response.data['status']))

    def test_member_create_organization(self):

        member_organization_create_data = {
            "name": "member Test Organization",
            "description": "This is a test organization by member."
        }

        #checks wether user with member role alone create organization

        self.user.roles.set([self.member_role_queryset])

        response = self.client.post(self.organization_url, data=member_organization_create_data, headers=self.header, format='json')

        self.assertEqual(response.data['status'], status.HTTP_401_UNAUTHORIZED,"Expected status code 401 UNAUTHORIZED, but got {0}".format(response.data['status']))


    def test_create_role(self):

        #checks wether user with all role alone create role

        self.user.roles.set(self.role_instance)
        
        organization_create_data = {
            "name": "Test role",
            "description": "This is a test role.",
            "organization":self.organization.pk
        }

        response = self.client.post(self.role_url, data=organization_create_data, headers=self.header, format='json')

        print(response.data)

        self.assertEqual(response.data['status'], status.HTTP_200_OK,"Expected status code 200 OK, but got {0}".format(response.data['status']))

    def test_super_admin_create_role(self):

        #checks wether user with all role alone create role

        self.user.roles.set([self.super_admin_role_queryset])
        
        organization_create_data = {
            "name": "Super admin Test role",
            "description": "This is a test role for super admin.",
            "organization":self.organization.pk
        }

        response = self.client.post(self.role_url, data=organization_create_data, headers=self.header, format='json')


        self.assertEqual(response.data['status'], status.HTTP_200_OK,"Expected status code 200 OK, but got {0}".format(response.data['status']))
