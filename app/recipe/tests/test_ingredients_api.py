from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.get(INGREDIENTS_URL)
        assert(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTest(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            '123456'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredients"""

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for authenticated users are returned"""

        user2= get_user_model().objects.create_user('other@test.com', '1234556')
        Ingredient.objects.create(user=user2, name='Vinager')
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successfull(self):
        """Test create a new ingredient"""
        payload = {
            'name': 'Cabbage'
        }

        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(user=self.user,
                                           name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test create invalid ingredient fails"""
        payload = {
            'name': ''
        }
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
