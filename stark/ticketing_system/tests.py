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
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


