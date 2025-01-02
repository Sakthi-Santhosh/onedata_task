from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class Organization(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Role(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(Organization, related_name="roles", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Username is required!')
        if not password:
            raise ValueError('Password is required!')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save()  # Don't pass self._db here
        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError('Username is required!')
        if not password:
            raise ValueError('Password is required!')
        
        user = self.model(username=username)
        user.set_password(password) 
        user.save() 
        return user

    def get_by_natural_key(self, username):

        return self.get(username=username)



class User(AbstractBaseUser):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 255, verbose_name='Username', unique = True)
    email = models.EmailField(max_length=254)
    organization = models.ForeignKey(Organization, verbose_name="Organization", on_delete=models.CASCADE,null=True,blank=True)
    roles = models.ManyToManyField(Role, verbose_name="roles")
    is_staff = models.BooleanField(verbose_name="Staff",default=True)
    is_superuser = models.BooleanField(verbose_name="Superuser",default=True)

    USERNAME_FIELD = 'username'

    object = CustomUserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
