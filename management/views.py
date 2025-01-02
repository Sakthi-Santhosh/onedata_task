from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import ProtectedError
from rest_framework.decorators import  authentication_classes,permission_classes
from .models import *
from .serializer import *
from .permission import permission_validation


#Login Funcationality

class LoginView(APIView):

    def post(self,request):

        data = request.data
        
        user_name = data.get('username')
        
        password=data.get('password')

        try:
            
            queryset = User.object.get(username=user_name)

        except Exception as err:
            
            return Response(
                {
                    "message":"User Doesnot Exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        user = authenticate(username=queryset.username,password=password)
        
        if user is not None:

            queryset.is_loggedin = True
            queryset.last_login = timezone.now()
            queryset.save()

            try:
                    
                token_queryset = Token.objects.get(user=queryset)
                    
                token_key = token_queryset.key
    
            except Token.DoesNotExist:
                
                token = Token.objects.create(user=queryset)
                
                token_key = token.key
                
            except Exception as err:
                pass

            res_data = {
                    "token":token_key,
                    "username":queryset.username,
                    "user_id":queryset.pk,
                    "organization":queryset.organization.name,
                    "roles":queryset.roles.all().values('name')
                }
                
                
            return Response(
                {
                    "data":res_data,
                    "message":"User Loggedin Sucessfully",
                    "status":status.HTTP_200_OK
                }
            )
            
        else:
            return Response(
                {
                    "message":"Username or Password is Invalid",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )
        

#Organization Funcationality
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrganizationView(APIView):


    #Create Organization
    def post(self,request):

        permission = permission_validation(request=request)


        #Permission Validation
        if permission['is_super_admin'] or permission['is_admin'] :


            request_data = request.data

            request_data['created_at'] = timezone.now()

            serializer = OrganizationSerializer(data=request_data)

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":"organization created sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":"organization not created",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        else:

            return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )

    #Retrieve Organization 
    def get(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Organization.objects.get(id=pk)

            serializer = OrganizationSerializer(queryset)

            return Response(
                    {
                        "data":serializer.data,
                        "message":"organization details retrieved sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
        
        except Organization.DoesNotExist:

            return Response(
                {
                    "message":"organization doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
    

    #Update Organization
    def put(self,request):

        try:

            pk = request.data.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Organization.objects.get(id=pk)

            request_data = request.data

            permission = permission_validation(request=request)

            #Permission Validation

            if permission['is_super_admin'] or permission['is_admin']:


                
                    
                serializer = OrganizationSerializer(queryset,data=request_data,partial=True)

                if serializer.is_valid():

                    #if admin and not super admin check wether it is same organization

                    if permission['is_super_admin'] == False and permission['is_admin'] == True:

                        if request.user.organization.pk != queryset.pk:

                            return Response(
                                {
                                    "message":"permission denied",
                                    "status":status.HTTP_401_UNAUTHORIZED
                                },status=status.HTTP_200_OK
                            )

                    serializer.save()

                    return Response(
                        {
                            "data":serializer.data,
                            "message":"organization updated sucessfully",
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
                else:

                    return Response(
                        {
                            "data":serializer.errors,
                            "message":"organization not updated",
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )

            else:

                return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )
        
        except Organization.DoesNotExist:

            return Response(
                {
                    "message":"organization doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

    #Delete Organization
        
    def delete(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Organization.objects.get(id=pk)

            permission = permission_validation(request=request)

            #Permission Validation

            if permission['is_super_admin'] or permission['is_admin']:

                #if admin and not super admin check wether it is same organization

                if permission['is_super_admin'] == False and permission['is_admin'] == True:

                    if request.user.organization.pk != queryset.pk:

                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )
                    
                queryset.delete()

                return Response(
                    {
                        "message":"organization deleted sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                    
            else:

                return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )

        except ProtectedError:

            return Response(
                {
                    "message":"please deleted the related items",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
        except Organization.DoesNotExist:

            return Response(
                {
                    "message":"organization doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )


#Organization List Funcationality

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrganizationListView(APIView):

    def post(self,request):

        search = request.data.get('search',"")

        queryset = Organization.objects.filter(name__icontains=search)

        serializer = OrganizationSerializer(queryset,many=True)

        return Response(
            {
                "data":serializer.data,
                "message":"organization list retrieved sucessfully",
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RoleView(APIView):


    #Create Role

    def post(self,request):

        permission = permission_validation(request=request)

        #Permission Validation

        if permission['is_super_admin'] or permission['is_admin'] :

            request_data = request.data

            
            
            serializer = RoleSerializer(data=request_data)

            if serializer.is_valid():

                #if admin and not super admin check wether it is same organization

                if  permission['is_super_admin'] == False and permission['is_admin']:

                    if request_data['organization'] != request.user.organization.pk:

                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )

                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":"role created sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":"role not created",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        else:

            return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )
        
    #Retrieve Role
        
    def get(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Role.objects.get(id=pk)

            serializer = RoleSerializer(queryset)

            response_data = serializer.data

            response_data['organization_name'] = queryset.organization.name

            return Response(
                    {
                        "data":response_data,
                        "message":"role details retrieved sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
        
        except Role.DoesNotExist:

            return Response(
                {
                    "message":"role doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    #Update Role
    def put(self,request):

        try:

            pk = request.data.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Role.objects.get(id=pk)

            request_data = request.data

            permission = permission_validation(request=request)

            #Permission Validation

            if permission['is_super_admin'] or permission['is_admin']:


                serializer = RoleSerializer(queryset,data=request_data,partial=True)

                if serializer.is_valid():

                    #if admin and not super admin check wether it is same Organization

                    if permission['is_super_admin'] == False and permission['is_admin'] == True:

                        if request.user.organization.pk != queryset.organization.pk:

                            return Response(
                                {
                                    "message":"permission denied",
                                    "status":status.HTTP_401_UNAUTHORIZED
                                },status=status.HTTP_200_OK
                            )

                    serializer.save()

                    return Response(
                        {
                            "data":serializer.data,
                            "message":"role updated sucessfully",
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
                else:

                    return Response(
                        {
                            "data":serializer.errors,
                            "message":"role not updated",
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )

            else:

                return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )
        
        except Role.DoesNotExist:

            return Response(
                {
                    "message":"role doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
    
    #Delete Role
    def delete(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            queryset = Role.objects.get(id=pk)

            permission = permission_validation(request=request)

            #Permission Validation

            if permission['is_super_admin'] or permission['is_admin']:

                #if admin and not super admin check wether it is same Organization

                if permission['is_super_admin'] == False and permission['is_admin'] == True:

                    if request.user.organization.pk != queryset.organization.pk:

                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )
                    
                queryset.delete()

                return Response(
                    {
                        "message":"role deleted sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                    
            else:

                return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )

        except ProtectedError:

            return Response(
                {
                    "message":"please deleted the related items",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
        except Role.DoesNotExist:

            return Response(
                {
                    "message":"role doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RoleListView(APIView):

    def post(self,request):

        search = request.data.get("search","")
        organization = request.data.get("organization",None)

        filter_condition = {}

        filter_condition['name__icontains'] = search

        if organization != None:

            filter_condition['organization'] = organization


        queryset = Role.objects.filter(**filter_condition)

        serializer = RoleSerializer(queryset,many=True)

        return Response(
            {
                "data":serializer.data,
                "message":"role list retrieved sucessfully",
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserView(APIView):

    def post(self,request):

        permission = permission_validation(request=request)

        #Permission Validation

        if permission['is_super_admin'] or permission['is_admin'] :

            request_data = request.data

            password = request_data['password']

            
            
            serializer = UserSerializer(data=request_data)

            if serializer.is_valid():

                #if admin and not super admin check wether it is same organization

                if  permission['is_super_admin'] == False and permission['is_admin']:

                    if request_data['organization'] != request.user.organization.pk:

                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )

                serializer.save()

                user_queryset = User.object.get(id=serializer.data['id'])
                user_queryset.set_password(password)
                user_queryset.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":"user created sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":"user not created",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        else:

            return Response(
                {
                    "message":"permission denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_200_OK
            )
        
    def get(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            permission = permission_validation(request=request)


            queryset = User.object.get(id=pk)

            if permission['is_super_admin'] == False and permission['is_admin']  == True:

                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_manager']  == True:
    
                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_admin'] == False and permission['is_admin'] == False and permission['is_member'] == True:

                if request.user.pk != queryset.pk:

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            serializer = UserSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":"user details retrieved sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )


        except User.DoesNotExist:

            return Response(
                {
                    "message":"user doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def put(self,request):

        try:

            pk = request.data.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            permission = permission_validation(request=request)


            queryset = User.object.get(id=pk)

            if permission['is_super_admin'] == False and permission['is_admin']  == True:

                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_manager']  == True:
    
                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_admin'] == False and permission['is_admin'] == False and permission['is_member'] == True:

                if request.user.pk != queryset.pk:

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            request_data = request.data
                
            serializer = UserSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":"user updated sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":"user not updated",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )

        except User.DoesNotExist:

            return Response(
                {
                    "message":"user doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def delete(self,request):

        try:

            pk = request.GET.get('id',None)

            if pk == None:

                return Response(
                    {
                        "message":"ID is required",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            permission = permission_validation(request=request)


            queryset = User.object.get(id=pk)

            if permission['is_super_admin'] == False and permission['is_admin']  == True:

                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_manager']  == True:
    
                if str(queryset.organization.pk) != str(request.user.organization.pk):

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK
                    )
                
            if permission['is_super_admin'] == False and permission['is_admin'] == False and permission['is_admin'] == False and permission['is_member'] == True:


                return Response(
                    {
                        "message":"permission denied",
                        "status":status.HTTP_401_UNAUTHORIZED
                    },status=status.HTTP_200_OK
                )
                
            queryset.delete()

            return Response(
                {
                    "message":"user deleted sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )


        except User.DoesNotExist:

            return Response(
                {
                    "message":"user doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except ProtectedError:

            return Response(
                {
                    "message":"delete related items",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserListView(APIView):

    def post(self,request):

        search = request.data.get("search","")

        filter_condition = {}

        filter_condition['username__icontains'] = search

        permission = permission_validation(request=request)

        if permission['is_super_admin'] == False:

            if permission['is_admin'] or permission['is_manager']:

                filter_condition['organization'] = request.user.organization.pk

            if permission['is_admin'] == False and permission['is_manager'] == False and permission['is_member'] == True:

                return Response(
                    {
                        "message":"permission denied",
                        "status":status.HTTP_401_UNAUTHORIZED
                    },status=status.HTTP_200_OK
                )
            
        queryset = User.object.filter(**filter_condition)

        serializer = UserSerializer(queryset,many=True)

        return Response(
                {
                    "data":serializer.data,
                    "message":"user list retrieved sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RoleAssignView(APIView):

    def post(self,request):

        try:

            permission = permission_validation(request=request)

            user_id = request.data.get('id',None)

            if user_id == None:

                    return Response(
                        {
                            "message":"user ID is required",
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            
            roles = request.data.get('roles')

            

            queryset = User.object.get(id=user_id)

            data = {
                "roles":roles
            }

            if permission['is_super_admin'] == False:

                if permission['is_admin'] :

                    if queryset.organization.pk != request.user.organization.pk:

                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )
                    
                if permission['is_admin'] == False and permission['is_manager'] == True:

                    if queryset.organization.pk != request.user.organization.pk:


                        return Response(
                            {
                                "message":"permission denied",
                                "status":status.HTTP_401_UNAUTHORIZED
                            },status=status.HTTP_200_OK
                        )
                    
                    else:

                        for role in roles:

                            role_queryset = Role.objects.get(id=role)

                            if role_queryset.name == "Super Admin":

                                return Response(
                                    {
                                        "message":"permission denied",
                                        "status":status.HTTP_401_UNAUTHORIZED
                                    },status=status.HTTP_200_OK
                                )

                if permission['is_admin'] == False and permission['is_manager'] == False and permission['is_member'] == True:

                    return Response(
                        {
                            "message":"permission denied",
                            "status":status.HTTP_401_UNAUTHORIZED
                        },status=status.HTTP_200_OK

                    )

            serializer = UserSerializer(queryset,data=data,partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":"user role updated sucessfully",
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":"user role not updated",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )

        except User.DoesNotExist:

            return Response(
                {
                    "message":"user doesnot exsist",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            
            return Response(
                {
                    "message":"something went wrong",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )















        



