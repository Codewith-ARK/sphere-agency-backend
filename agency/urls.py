from django.urls import path

from .views import CreateAgency

urlpatterns = [
    path('new/', CreateAgency.as_view())
]