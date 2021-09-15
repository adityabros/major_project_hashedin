from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

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

    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    reporter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporting_user')
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigned_user')


class User_Profile(models.Model):

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    role = models.CharField(max_length=15)





