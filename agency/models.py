from django.db import models

from users.models import CustomUser, Employee

# Create your models here.
class Agency(models.Model):
    title = models.CharField(max_length=255)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owner')
    employees = models.ManyToManyField(Employee, related_name='agency_employees')
    type = models.CharField()