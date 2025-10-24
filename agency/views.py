from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.status import *

from .serializers import AgencyCreateSerializer
from .models import Agency
# Create your views here.
class CreateAgency(generics.CreateAPIView):
    serializer_class = AgencyCreateSerializer
    queryset = Agency.objects.all()