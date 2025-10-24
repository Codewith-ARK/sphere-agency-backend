from rest_framework import serializers

from .models import Task
from users.serializers import EmployeeDetailSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        
class TaskDetailSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_assigned_to(self, obj):
        if not obj.assigned_to:
            return None
        data = EmployeeDetailSerializer(obj.assigned_to, context=self.context).data
        user = getattr(obj.assigned_to, "user", None)
        if user:
            data["user"] = {k: getattr(user, k, None) for k in ("id", "username", "email", "first_name", "last_name")}
        return data['user']
        
class TaskSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['assigned_to', 'objective', 'campaign', 'notes']