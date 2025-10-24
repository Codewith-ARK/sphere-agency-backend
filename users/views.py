from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count

from .models import CustomUser, Employee
from .serializers import (
    UserRegistrationSerializer,
    EmployeeSerializer,
    UserSerializer,
    LoginSerializer,
    UserSummarySerializer
)
from tasks.models import Task
from tasks.serializers import TaskDetailSerializer, TaskSummarySerializer
from campaigns.models import Campaign

import json


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"user": serializer.data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class FetchUser(views.APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response(status=404)
        
        data = {}
        data = UserSerializer(user).data
        
        if user.role == 'client':
            campaigns = Campaign.objects.filter(created_by=user).all()
            serialized_campaigns = CampaignSerializer(campaigns, many=True).data
            data['campaigns'] = serialized_campaigns
        elif user.role == 'employee':
            tasks = Task.objects.filter(assigned_to=user.employee).all()
            serialized_tasks = TaskSummarySerializer(tasks, many=True).data
            data['employee_profile']['tasks'] = serialized_tasks

        return Response(data, status=200)


class FetchAllUser(generics.ListAPIView):
    serializer_class = UserSummarySerializer
    queryset = CustomUser.objects.all()


from campaigns.serializers import CampaignSerializer


class Dashboard(views.APIView):
    def get(self, request):
        user = request.user

        if user.role == "employee":
            tasks = Task.objects.filter(assigned_to=user.employee).all().order_by('priority', 'hours_required')
            serialized_tasks = TaskDetailSerializer(tasks, many=True).data
            return Response(
                {
                    "tasks": serialized_tasks,
                },
                status=status.HTTP_200_OK,
            )

        if user.role == "client":
            try:
                campaign = Campaign.objects.filter(created_by=user).all().order_by('-created_at')
                serialized_campaigns = CampaignSerializer(campaign, many=True).data
                return Response(
                    {
                        "campaigns": serialized_campaigns,
                    },
                    status=status.HTTP_200_OK,
                )
            except Campaign.DoesNotExist:
                return Response(
                    {
                        "campaigns": serialized_campaigns,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        if user.role in ["admin", "superadmin"]:
            try:
                campaign = Campaign.objects.values("status").annotate(total=Count("id"))
                # serialized_campaigns = CampaignSerializer(campaign, many=True).data
                tasks = Task.objects.values("status").annotate(total=Count("id"))
                # serialized_tasks = TaskDetailSerializer(tasks, many=True).data
                return Response(
                    {
                        # "campaigns": serialized_campaigns,
                        # 'tasks': serialized_tasks,
                        "count": {
                            "campaigns": campaign,
                            "tasks": tasks,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            except Campaign.DoesNotExist:
                return Response(
                    {"campaigns": {}, "tasks": {}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class FetchSkills(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class UpdateSkills(views.APIView):
    def patch(self, request, pk):
        skills = request.data.get("skills", "")
        employee = Employee.objects.get(user__id=pk)

        if employee.skills:
            # append new skills
            employee.skills += f",{skills}"
        else:
            # initialize if empty
            employee.skills = skills

        employee.save()

        serialized = EmployeeSerializer(employee).data
        return Response(serialized, status=200)

