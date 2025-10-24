from django.db import models

from users.models import CustomUser

# Create your models here.
class Campaign(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ('generating', 'Generating'),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='campaigns')
    title = models.CharField(max_length=255)
    type = models.CharField()
    platform = models.CharField()
    budget = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    status = models.CharField(max_length=128, default="pending", choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    start_data = models.DateField(null=True)
    end_date = models.DateField(null=True)
    duration = models.IntegerField()
    
    notes = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.duration} Day(s) : {self.platform} Campaign || {self.title}"
    
class Contract(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
class ContractClause(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="clauses", null=True)
    title = models.CharField()
    text = models.TextField()
    explanation = models.TextField()
    
    def __str__(self):
        return f"{self.title} for {self.contract.campaign.title}"