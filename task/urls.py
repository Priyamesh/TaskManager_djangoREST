from django.urls import path
from rest_framework.authtoken import views
from task.views import Home,TasksGetPost

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('api-token-auth', views.obtain_auth_token),
    path('tasks',TasksGetPost.as_view(),name='taksgetpost'),
]