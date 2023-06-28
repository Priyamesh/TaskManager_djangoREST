from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json

from task.models import Tasks
from task.serializer import TaskSerializer
# Create your views here.

class Home(APIView):

    def get(self,request):
        return Response(data={'message':'working fine'},status=status.HTTP_200_OK)

class TasksGetPost(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        print(user.username)
        tasks = Tasks.objects.filter(user=user.id)
        serializer = TaskSerializer(tasks,many=True)
        return Response(data={'tasks':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        user = request.user
        data = json.loads(request.body)
        data['user']=user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'task':serializer.data},status=status.HTTP_201_CREATED)

        return Response(data={'error':serializer.errors},status=status.HTTP_404_NOT_FOUND)