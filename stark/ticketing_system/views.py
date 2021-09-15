from django.shortcuts import render
from rest_framework import viewsets

from . import serializers,models
from django.db.models import Q

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