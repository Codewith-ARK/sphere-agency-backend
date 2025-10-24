from django.urls import include, path

from .views import *

urlpatterns=[
    path("<int:pk>/", FetchUser.as_view(), name="fetch-user"),
    path("all/", FetchAllUser.as_view(), name="login"),
    path("new/", CreateUserView.as_view(), name="registration"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("dashboard/", Dashboard.as_view(), name="login"),
    
    path("<int:pk>/skill/", FetchSkills.as_view(), name="login"),
    path("<int:pk>/skill/update/", UpdateSkills.as_view(), name="login"),
]