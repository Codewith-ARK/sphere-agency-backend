from rest_framework import serializers

from .models import *
from tasks.serializers import TaskDetailSerializer

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"
        
class ClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractClause
        fields = "__all__"        

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        
class ContractDetailSerializer(serializers.ModelSerializer):
    clauses = ClauseSerializer(many=True, read_only=True)
    class Meta:
        model = Contract
        fields = "__all__"
                
class CampaignDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True)
    contract = ContractDetailSerializer()
    class Meta:
        model = Campaign
        fields = '__all__'
        
