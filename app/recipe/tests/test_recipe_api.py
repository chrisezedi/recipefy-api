"""
Tests for recipe APIs.
"""
from decimal import Decimal


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# from core.models import (
#     Recipe,
# )

# from recipe.serializers import (
#     RecipeSerializer
# )

RECIPE_URL = reverse('recipe:recipe-list')


class privateRecipeApiTests(TestCase):
    """create recipe test"""
    """
    Possible test cases
     - create recipe success
     - test invalid data
     - test price is decimal
    """

    def setUp(self):
        user = get_user_model().objects.create(
            email='user@example.com', password='testpassword')
        self.client = APIClient()
        self.user = user
        self.client.force_authenticate(self.user)

    def test_create_recipe(self):
        payload = {
            'name': 'recipe1',
            'description': 'recipe1 desc',
            'time_minutes': 30,
            'price': Decimal(300),
            'link': 'recipe1.com'
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])
