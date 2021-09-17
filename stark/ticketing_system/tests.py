from django.test import TestCase,Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


from . import models,serializers

class getAllTestProject(TestCase):
    project_data = {
            "title": 'Dummy Project',
            "description": 'Dummy testing',
            "creator": 1
        }
    
    test_issue_data = {
            "type":"BUG",
            "description":"My first Issue test",
            "status":"open",
            "title":"Issue title",
            "project":1,
            "reporter":1,
            "assignee":1,
            "labels":[]
        }
    test_label_data = {
        "name":"Test Label"
    } 

    test_watcher_data = {
        "user":1,
        "issue":1,
    }
    client = Client()

    credentials = {"username":"admin","password":"admin"}
    
    response = client.post('/api/token/', data=credentials, format="json")
    
    access_token = 'Bearer '+response.data['access']
    
    client = Client()
    def setUp(self):
        
        user = User.objects.create(username="admin",password="admin")
        
        proj = models.Project.objects.create(title='Test 1', description='My first test', creator=user)
        lbl = models.Labels.objects.create(name="Dummy Label")
        # models.Issue.objects.create(title='Test 1', description='My first test', type="BUG",status="OPEN",project=proj,reporter=user,assignee=user)
        
    def test_all_GET(self):
        
        client = self.client

        #Getting all Projects

        response = client.get('/ticketing_system/project/',HTTP_AUTHORIZATION=self.access_token)
        # get data from db
        projects = models.Project.objects.all()
        serializer = serializers.ProjectSerializer(projects, many=True)
        print("response data = ",response.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        #Getting all Issues

        response = client.get('/ticketing_system/issues/',HTTP_AUTHORIZATION=self.access_token)
        # get data from db
        issues = models.Issue.objects.all()
        serializer = serializers.IssueSerializer(issues, many=True)
        # print(" res data = ",response.data)
        # print(" ser data = ",serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Getting all Labels
        response = client.get('/ticketing_system/labels/',HTTP_AUTHORIZATION=self.access_token)
        labels = models.Labels.objects.all()
        serializer = serializers.LabelSerializer(labels, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Getting all Watchers
        response = client.get('/ticketing_system/watcher/',HTTP_AUTHORIZATION=self.access_token)
        watchers = models.Watcher.objects.all()
        serializer = serializers.WatcherSerializer(issues, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Getting all Users
        response = client.get('/ticketing_system/users/',HTTP_AUTHORIZATION=self.access_token)
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Getting all Comments
        response = client.get('/ticketing_system/comments/',HTTP_AUTHORIZATION=self.access_token)
        users = models.Comments.objects.all()
        serializer = serializers.CommentsSerializer(users, many=True)
        
        print("response comments = ",response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




        #################POST Requests Test##################



        response = client.post('/ticketing_system/project/', data=self.project_data, format="json",HTTP_AUTHORIZATION=self.access_token)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        #posting in Issues

        response = client.post('/ticketing_system/issues/', data=self.test_issue_data, format="json",HTTP_AUTHORIZATION=self.access_token)
        print("post resp get = ",response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #posting in Labels

        response = client.post('/ticketing_system/labels/', data=self.test_label_data, format="json",HTTP_AUTHORIZATION=self.access_token)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #posting in Watcher

        response = client.post('/ticketing_system/watcher/', data=self.test_watcher_data, format="json",HTTP_AUTHORIZATION=self.access_token)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

 





