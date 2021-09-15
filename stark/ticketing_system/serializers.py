from rest_framework import serializers

from .models import *



class IssueSerializer(serializers.ModelSerializer):
   class Meta:
       model = Issue
       fields = ('description', 'type', 'status','title','project','reporter','assignee')

    #    fields = ('__all__')

class ProjectSerializer(serializers.ModelSerializer):
   issues = IssueSerializer(many=True,read_only=True) 
   class Meta:
       model = Project
       fields = ('description', 'title', 'creator','issues')
    #    fields = ('__all__')