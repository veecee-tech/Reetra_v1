from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    
    def create_user(self,username, phone, email, fullname, password=None):

        if username is None:
            raise ValueError("users Should Have an account number")

        if email is None:
            raise ValueError("users Should Have an email")
        
        if fullname is None:
            return ValueError("please enter your full name")
        
        
        user = self.model(username=username, phone=phone, email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, phone=None, password=None):
    
        if password is None:
            raise ValueError("password should not be none")

        user = self.create_user(username=username, email=email,phone=phone, password=password)

        user.is_superadmin= True
        user.is_staff = True
        user.is_admin = True
        user.role = 1
        user.is_active = True
        
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser):

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20)

    #receipt unique number
    number_count = models.IntegerField(default=0)
    trial_version_exceeded = models.BooleanField(default=False)
    #required
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email',]

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def get_number_count(self):
        return self.number_count
    
    def get_is_trial_version_exceeded(self):
        return self.trial_version_exceeded

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    
  
    user = models.OneToOneField(
        UserAccount,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='userprofile', null=False)
    business_name = models.CharField(blank=True, null=True, max_length=255)
    business_address = models.CharField(blank=True, null=True, max_length=255)
    business_logo = models.ImageField(upload_to='logo/', null=True)
    


@receiver(post_save, sender=UserAccount)
def create_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
    else:
        pass


