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

class TaskUpdation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        user = request.user
        try:
            task = Tasks.objects.get(user = user.id, id=id)
            serializer = TaskSerializer(task)
            return Response(data={'task':serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response(data={'message':'Task doesnt exist'},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        user = request.user
        data = json.loads(request.body)
        data['user']=user.id
        try:
            task = Tasks.objects.get(user = user.id, id=id)
        except Exception as err:
            return Response(data={'message':'task not found'},status=status.HTTP_400_BAD_REQUEST)
        

        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'task':serializer.data},status=status.HTTP_201_CREATED)
        return Response(data={'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        user = request.user

        try:
            task = Tasks.objects.get(user = user.id, id = id)
            serializer = TaskSerializer(task)
            task.delete() 
            return Response(data={'task':serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response(data={'message':'Task does not exists'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
    