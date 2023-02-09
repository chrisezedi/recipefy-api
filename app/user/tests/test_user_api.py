"""Tests For User API"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


payload = {
    'email': 'user@example.com',
    'password': 'testpassword123',
    'name': 'ekene'
}


class publicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_already_exists(self):
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        payload.update({'password': 'pass'})
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_user_success(self):
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertTrue(user_exists)
        self.assertNotIn('password', res.data)
