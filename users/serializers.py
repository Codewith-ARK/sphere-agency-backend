from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import authenticate

from .models import CustomUser, Employee

class UserRegistrationSerializer(serializers.ModelSerializer):

    skills = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "contact",
            "skills",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        skills = validated_data.pop("skills", None)

        with transaction.atomic():
            user = CustomUser(**validated_data)
            user.set_password(password)
            user.save()

            if user.role == "employee":
                Employee.objects.create(user=user, skills=skills)

        return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id',"skills"]
        extra_kwargs = {"user": {"read_only": True}}
        
class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password =  attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError("Incorrect email or password", code='authorization')

        else:
            raise serializers.ValidationError("Email and Password are required.", code="authorization")

        attrs["user"] = user
        return attrs

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role']


class UserSerializer(serializers.ModelSerializer):
    employee_profile = EmployeeSerializer(source='employee')
    class Meta:
        model = CustomUser
        fields = [
            'id',
            "first_name",
            "last_name",
            "email",
            "role",
            "contact",
            "employee_profile",
        ]