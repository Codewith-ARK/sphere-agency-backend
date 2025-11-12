from django.urls import path, include

from tasks.views import UpdateTaskStatus, FetchTask, FetchAllTask, TotalTaskHours

urlpatterns = [
    path('',FetchAllTask.as_view(), name="fetch-all-task"),
    path('all/',TotalTaskHours.as_view(), name="fetch-task"),
    path('<int:pk>/',FetchTask.as_view(), name="fetch-task"),
    path('<int:pk>/update/',UpdateTaskStatus.as_view(), name="update-task"),
]