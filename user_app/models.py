#host_app/models.py
from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.conf import settings
from role_app.models import Role
from django.utils.text import slugify


# Create your models here.
class Department(models.Model):
    dep_code = models.SlugField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    # dep_code = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.slug =  slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser, PermissionsMixin):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.ManyToManyField(Role, related_name='role', blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email