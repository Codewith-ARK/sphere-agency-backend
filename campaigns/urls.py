from django.urls import path, include

from .views import *

urlpatterns = [
    path("new/", CreateCampaign.as_view(), name="create-campaign"),
    path("new/quote/", QuoteCampaignBudget.as_view()),

    path("all/", GetAllCampaign.as_view()),
    path("<int:pk>/", GetCampaign.as_view()),
    path("<int:pk>/update/", UpdateCampaignStatus.as_view()),
    path("<int:pk>/generate/", GenerateContract.as_view()),
    
    path("test/", Test.as_view()),
]