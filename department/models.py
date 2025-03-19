from django.db import models
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