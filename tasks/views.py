from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.status import *

from .models import Task
from .serializers import TaskSerializer, TaskDetailSerializer
from django.db.models import Sum

class FetchAllTask(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
    def get(self, request):
        user = request.user
        qs = self.queryset.order_by('priority', 'hours_required')
        serializer = self.serializer_class
        tasks = {}

        if user.role == 'client':
            tasks = qs.filter(campaign__created_by=user).all()
        elif user.role == 'employee':
            tasks = qs.filter(assigned_to=user.employee).all()
        else:
            tasks = qs.all()

        serialized = serializer(tasks, many=True).data
        return Response(serialized, status=HTTP_200_OK)


class FetchTask(generics.RetrieveAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()
    lookup_field = 'pk'
    
class TotalTaskHours(views.APIView):
    def get(self, request):
        user = getattr(self, "request", None).user if getattr(self, "request", None) else None
        qs = Task.objects.all()

        if user and getattr(user, "role", None) == "client":
            qs = qs.filter(campaign__created_by=user)
        elif user and getattr(user, "role", None) == "employee":
            qs = qs.filter(assigned_to=user.employee)

        agg = qs.values("priority").annotate(total_hours=Sum("hours_required")).order_by("priority")
        result = {item["priority"]: (item["total_hours"] or 0) for item in agg}

        return Response(result, status=HTTP_200_OK)

class UpdateTaskStatus(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'pk'