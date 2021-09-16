from django.test import TestCase,Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


from . import models,serializers

class getAllTest(TestCase):

    def setUp(self):
        
        user = User.objects.create(username="admin2",password="passsword")
        
        models.Project.objects.create(title='Test 1', description='My first test', creator=user)


    def test_get_all_projects(self):
        
        client = Client()
        response = client.get('/ticketing_system/project/')
        # get data from db
        projects = models.Project.objects.all()
        serializer = serializers.ProjectSerializer(projects, many=True)
        print(" res data = ",response.data)
        print(" ser data = ",serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_post_in_project(self):
        
        self.project_data = {
            "title": 'Dummy Project',
            "description": 'Dummy testing',
            "creator": 2
        }

        client = Client()

        response = client.post('/ticketing_system/project/', data=self.project_data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



