from stark_industries.settings import LANGUAGE_CODE
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.PROTECT,related_name='Project')

class Labels(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Issue(models.Model):

    
    issue_types = [
        ('BUG', 'BUG'),
        ('TASK', 'TASK'),
        ('STORY', 'STORY'),
        ('EPIC', 'EPIC'),]

    issue_status = [
        ('open', 'OPEN'),
        ('in_progress', 'IN_PROGRESS'),
        ('in_review', 'IN_REVIEW'),
        ('code_complete', 'CODE_COMPLETE'),
        ('done', 'DONE'),
        ]
    

    description = models.TextField()
    type = models.CharField(choices=issue_types,max_length=15,default='BUG')
    status = models.CharField(choices=issue_status,max_length=15,default='open')
    title = models.CharField(max_length=200)

    project = models.ForeignKey(Project, on_delete=models.PROTECT,related_name='issues')

    reporter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporting_user')
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigned_user')
    labels = models.ManyToManyField(Labels)


class User_Profile(models.Model):

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    role = models.CharField(max_length=15)

class Watcher(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)

#Event Log
#Comment
#Label - many to many with Issues
#  labels (only contain labels), label_link_issue - (label_id,issue_id)
# Label_issue_link
#Watcher

# language tag
# c++      oop
# python   oop

# tag
# oop 
# link LANGUAGE
# 1 1
# 2 1






