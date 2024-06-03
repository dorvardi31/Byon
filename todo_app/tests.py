from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):
    def test_create_task(self):
        url = reverse('task-list-create')
        data = {'title': 'Test Task', 'description': 'Test Description', 'status': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_read_tasks(self):
        url = reverse('task-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_retrieve_task(self):
        task = Task.objects.create(title='Test Task', description='Test Description', status=False)
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], task.title)

    def test_update_task(self):
        task = Task.objects.create(title='Initial Task', description='Initial Description', status=False)
        url = reverse('task-detail', args=[task.id])
        data = {'title': 'Updated Task', 'description': 'Updated Description', 'status': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(title='Task to be deleted', description='Delete Description', status=False)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

