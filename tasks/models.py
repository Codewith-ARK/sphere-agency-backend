from django.db import models

from users.models import Employee
from campaigns.models import Campaign

class Task(models.Model):
    STATUS_CHOICES = [
        ("rejected", "Rejected"),
        ("pending", "Pending"),
        ("to_do", "To-Do"),
        ("in_progress", "In-Progress"),
        ("completed", "Completed"),
    ]
    
    PRIORITY_CHOICES = [
        ('high', "High"),
        ('medium', "Medium"),
        ('low', "Low"),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField()
    objective = models.TextField()
    priority = models.CharField(choices=PRIORITY_CHOICES)
    hours_required = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='tasks')
    
    notes = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.id}. {self.campaign.title} : {self.title} "