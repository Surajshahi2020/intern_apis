from django.urls import path
from internapp.api.viewsets.accounts import (
    UserViewSet,
    LoginViewSet,
    TaskCreateViewSet,
    TaskListViewSet,
    TaskEditViewSet,
    SubmitTaskViewSet,
    SubmitTaskEditViewSet,
    TaskSubmitListViewSet,
    TaskListInternViewSet,
)

urlpatterns = [
    path("account-registration/", UserViewSet.as_view()),
    path("account-login/", LoginViewSet.as_view()),
    path("task-create/", TaskCreateViewSet.as_view()),
    path("task-list-supervisor/", TaskListViewSet.as_view()),
    path("task-edit/<str:pk>/", TaskEditViewSet.as_view()),
    path("submit-task/", SubmitTaskViewSet.as_view()),
    path("submit-task-edit/<str:pk>", SubmitTaskEditViewSet.as_view()),
    path("submitted-task-list/", TaskSubmitListViewSet.as_view()),
    path("task-list-intern/", TaskListInternViewSet.as_view()),
]
