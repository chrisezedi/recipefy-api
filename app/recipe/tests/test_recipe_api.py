"""
Tests for recipe APIs.
"""
from decimal import Decimal


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Recipe,
)

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer
)

RECIPE_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    defaults = {
        'name': 'recipe1',
        'description': 'recipe1 desc',
        'time_minutes': 30,
        'price': Decimal(300),
        'link': 'recipe1.com'
    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def create_user(**params):
    defaults = {
        'email': 'user@example.com',
        'password': 'testpassword'
    }

    defaults.update(params)
    return get_user_model().objects.create(**params)


def detail_url(id):
    return reverse('recipe:recipe-detail', args=[id])


class privateRecipeApiTests(TestCase):
    """Private Recipe API Tests"""

    def setUp(self):
        """before each setup"""
        user = create_user()
        self.client = APIClient()
        self.user = user
        self.client.force_authenticate(self.user)

    def test_create_recipe(self):
        """create recipe"""
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

    def test_list_all_recipes(self):
        """retrieve all recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_all_auth_user_recipes(self):
        other_user = create_user(
            email='otheruser@example.com', password='inspiredOTUS')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(recipe.description, res.data['description'])
        self.assertEqual(res.data, serializer.data)
