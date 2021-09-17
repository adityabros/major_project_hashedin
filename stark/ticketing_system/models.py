from stark_industries.settings import LANGUAGE_CODE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

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

    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='issues')

    reporter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporting_user')
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigned_user')
    labels = models.ManyToManyField(Labels,blank=True)

class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='logging_user')
    time_taken = models.IntegerField()
    work_description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

class User_Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.PROTECT,related_name='user_profile')
    roles = [
        ('admin', 'Admin'),
        ('pm', 'Project Manager'),
        ('standard', 'Standard'),
        ]
    role = models.CharField(max_length=15,choices=roles,default="admin")

class Watcher(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)

class WatcherProject(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

class event_logs(models.Model):

    updated_field = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)
    previous_value = models.CharField(max_length=20)
    new_value = models.CharField(max_length=20)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)

@receiver(post_save, sender=event_logs)
def track_events(sender, instance, created, **kwargs):

    subject = 'Event {} for Issue : {} changed'.format(instance.updated_field,instance.issue.title)
    message = 'Old Value : {} , New Value : {}'.format(instance.previous_value,instance.new_value)
    from_email = 'aditya201196@yahoo.com'
    watchers = Watcher.objects.filter(issue=instance.issue)
    email_ids = [w.user.email for w in watchers]
    
    project_watchers = WatcherProject.objects.filter(project=instance.issue.project)
    email_ids += [w.user.email for w in project_watchers]
    print("wooops")
    send_mail(subject, message, from_email, email_ids+['aditya201196@yahoo.com'])
    try:
        send_mail(subject, message, from_email, email_ids+['aditya201196@yahoo.com'])
    except :
        pass

class Comments(models.Model):
    
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(null=True)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)


@receiver(post_save, sender=Issue)
def create_watchers(sender, instance, created, **kwargs):
    if created:
        #Assignee and Reporters are default watchers
        Watcher.objects.create(user=instance.assignee,issue=instance)
        Watcher.objects.create(user=instance.reporter,issue=instance)
    



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.user_profile.save()
    except:
        pass


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






