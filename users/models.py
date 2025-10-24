from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import json


# Create your views here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("client", "Client"),
        ("employee", "Employee"),
        ("agency_owner", "Agency Owner"),
    ]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES)
    gender = models.CharField(choices=GENDER_CHOICES)
    contact = models.CharField(null=True, max_length=256)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee')
    skills = models.CharField(null=True, blank=True)
    job_title = models.CharField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    # {
    #     parent_skill: {
    #         name: foo, proficiency: [1 - 5]
    #     }
    # }

    def set_skills(self, val):
        self.skills = json.dumps(val)

    def get_skills(self):
        return json.loads(self.skills)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"