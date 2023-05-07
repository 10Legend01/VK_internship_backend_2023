from django.test import TestCase
from django.urls import reverse

from .models import User

import json


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User(username='123',)
        self.user1.save()
        self.user2 = User(username='456',)
        self.user2.save()

    def test_user_creation(self):
        self.assertEqual(self.user1.username, '123')
        self.assertEqual(self.user1.id, 1)
        self.assertEqual(self.user2.username, '456')
        self.assertEqual(self.user2.id, 2)

    def test_get_users(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, 200)
        content = [{'id': 1, 'username': '123'}, {'id': 2, 'username': '456'}]
        self.assertEqual(json.loads(resp.content), content)

    def test_user_login(self):
        resp = self.client.post(
            "/users/",
            {'username': '789'}
        )
        content = {'id': 3, 'username': '789'}
        self.assertEqual(json.loads(resp.content), content)

        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, 200)
        content = [{'id': 1, 'username': '123'}, {'id': 2, 'username': '456'}, {'id': 3, 'username': '789'}]
        self.assertEqual(json.loads(resp.content), content)
