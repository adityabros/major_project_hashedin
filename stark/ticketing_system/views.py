from django.shortcuts import render
from rest_framework import viewsets,generics
from django.contrib.auth.models import User

from . import serializers,models
from django.db.models import Q
from rest_framework.permissions import AllowAny 
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
   queryset = models.Project.objects.all()
   serializer_class = serializers.ProjectSerializer

   def get_queryset(self):
        queryset = models.Project.objects.all()
        title = self.request.query_params.get('title', None)
        id = self.request.query_params.get('id', None)

        if id:
            queryset = queryset.filter(id=id)
        elif title:
            queryset = queryset.filter(title__iexact=title)
        return queryset
    
   def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = serializers.UpdateProjectSerializer

        return serializer_class



class IssueViewSet(viewsets.ModelViewSet):
   queryset = models.Issue.objects.all()
   serializer_class = serializers.IssueSerializer

   def get_queryset(self):
        queryset = models.Issue.objects.all()
        title = self.request.query_params.get('title', None)
        id = self.request.query_params.get('id', None)
        description = self.request.query_params.get('description', None)
        if id:
            queryset = queryset.filter(id=id)
        elif description:
            queryset = queryset.filter(description__icontains=description)
        elif title:
            queryset = queryset.filter(title__iexact=title)
        return queryset

   def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = serializers.UpdateIssueSerializer

        return serializer_class 

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = serializers.UserSerializer

   def get_queryset(self):
        queryset = User.objects.all()
        
        return queryset

class LabelViewSet(viewsets.ModelViewSet):
   queryset = models.Labels.objects.all()
   serializer_class = serializers.LabelSerializer

class WatcherViewSet(viewsets.ModelViewSet):
   queryset = models.Watcher.objects.all()
   serializer_class = serializers.WatcherSerializer

class CommentsViewSet(viewsets.ModelViewSet):
   queryset = models.Comments.objects.all()
   serializer_class = serializers.CommentsSerializer
