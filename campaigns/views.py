from rest_framework import views, generics, status
from rest_framework.response import Response
from django.db.models import Count
from django.db import transaction

from .models import Campaign, Contract
from .serializers import *
from .utils import generate_budget, generate_and_save_tasks
from tasks.models import Task
from tasks.serializers import TaskSerializer
from users.models import Employee, CustomUser

import json, threading


class CreateCampaign(generics.CreateAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UpdateCampaignStatus(views.APIView): 
    @transaction.atomic
    def patch(self, request, pk):
        action = request.data.get("action")
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # prevent re-approval or re-rejection
        if campaign.status in ["approved", "rejected"]:
            return Response({"status": campaign.status}, status=200)

        if action == "rejected":
            user_note = request.data.get("notes" or "")
            campaign.notes = user_note
            campaign.status = action
            campaign.save()

            return Response(
                {
                    "message": "Updated",
                    "status": campaign.status,
                },
                status=status.HTTP_200_OK,
            )

        # Gather employee/task data for LLM
        employees = Employee.objects.annotate(task_count=Count("tasks")).values(
            "id", "user__email", "task_count", 'skills'
        )
        print(employees)
        campaign_data = CampaignSerializer(campaign).data
        client_info = campaign.created_by.get_full_name()
        threading.Thread(target=generate_and_save_tasks, args=(campaign,employees)).start()
        threading.Thread(target=generate_and_save_contract, args=(dict(campaign_data), client_info)).start()

        campaign.status = 'generating'
        campaign.save()

        # Attach campaign id to each task
        return Response(
            {
                # "message": f"Created {len(serializer.data)} task(s)",
                "status": campaign.status,
            },
            status=200,
        )


class GetCampaign(generics.RetrieveAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignDetailSerializer
    lookup_field = "pk"


class GetAllCampaign(generics.ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSummarySerializer
    ordering = ["-created_at"]

    def get(self, request):
        user = request.user
        qs = self.queryset.order_by('-created_at')
        serializer = self.serializer_class
        campaigns = {}
        
        if user.role == "client":
            campaigns = qs.filter(created_by=user)
        elif user.role == 'employee':
            campaigns = qs.filter(tasks__assigned_to=user.employee)
        else:
            campaigns = qs.all()
            
        serialized = serializer(campaigns, many=True).data
        return Response(serialized, status=status.HTTP_200_OK)


class QuoteCampaignBudget(views.APIView):
    serializer_class = CampaignSerializer

    def post(self, request):
        try:
            campaign_data = request.data
            serializer = self.serializer_class(data=campaign_data)
            serializer.is_valid(raise_exception=True)

            validated = serializer.validated_data

            structured = {
                "title": validated.get("title"),
                "campaignType": validated.get("type"),
                "platform": validated.get("platform"),
                "duration": f"{validated.get("duration")} Days",
            }

            quote = generate_budget(json.dumps(structured))
            return Response(quote[0], status=200)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchCampaign(generics.RetrieveAPIView):
    serializer_class = CampaignDetailSerializer
    queryset = Campaign.objects.all()
    lookup_field = "pk"

from .utils import generate_and_save_contract

class Test(views.APIView):
    def get(self, request):
        id = request.data.get('id')
        
        campaign = Campaign.objects.get(id=id)
        tasks = Task.objects.filter(campaign=campaign).all()
        
        task_data = TaskSerializer(tasks, many=True).data
        campaign_data = CampaignSerializer(campaign).data
        
        
        response = generate_and_save_contract(campaign_data, task_data)
        return Response(response, status=200)
        
class GenerateContract(views.APIView):
    def post(self, request, pk):
        campaign = Campaign.objects.get(id=pk)
        campaign_data = CampaignSerializer(campaign).data
        client_info = campaign.created_by.get_full_name()
        response = generate_and_save_contract(dict(campaign_data), client_info)
        return Response(response, status=200)
        