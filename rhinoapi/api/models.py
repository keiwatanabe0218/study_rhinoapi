from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Object(models.Model):
    title = models.CharField(max_length=50)
    objs = models.CharField(blank=True, max_length=1000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title