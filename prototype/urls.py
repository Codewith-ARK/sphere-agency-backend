from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('campaign/', include('campaigns.urls')),
    path('task/', include('tasks.urls')),
    path('agency/', include('agency.urls')),
]
