"""
Tests for the tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='testpass234'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


def detail_url(tag_id):
    """Create and return a tag details url."""
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagsApiTests(TestCase):
    """Tests unauthorized api requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test get api without authorization."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,  status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests authenticated api requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Tests retriving a list of tags."""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tests list of tags is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name='After dinner')

        payload = {'name': 'dessert'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tags(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(id=tag.id)
        self.assertFalse(tags.exists())

    # def test_filter_tags_assigned_to_recipes(self):
    #     """Test listing tags by those assigned to recipes."""
    #     in1 = Tags.objects.create(user=self.user, name='Apple')
    #     in2 = Tags.objects.create(user=self.user, name='Turkey')
    #     recipe = Recipe.objects.create(
    #         title='Apple Crumble',
    #         time_minutes=5,
    #         price=Decimal('4.59'),
    #         user=self.user
    #     )
    #     recipe.ingredients.add(in1)
    #     res=self.client.get(INGREDIENT_URL, {'assigned_only': 1})
    #     s1 = IngredientSerializer(in1)
    #     s2 = IngredientSerializer(in2)
    #     self.assertIn(s1.data, res.data)
    #     self.assertNotIn(s2.data, res.data)

    # def test_filtered_ingredients_unique(self):
    #     """Test filtered ingredients return a unique list."""
    #     in1 = Tags.objects.create(user=self.user, name='Apple')
    #     Tags.objects.create(user=self.user, name='Turkey')
    #     recipe1 = Recipe.objects.create(
    #         title='Apple Crumble',
    #         time_minutes=5,
    #         price=Decimal('4.59'),
    #         user=self.user
    #     )
    #     recipe2 = Recipe.objects.create(
    #         title='Chicken Shawai',
    #         time_minutes=30,
    #         price=Decimal('459'),
    #         user=self.user
    #     )
    #     recipe1.ingredients.add(in1)
    #     recipe2.ingredients.add(in1)

    #     res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

    #     self.assertEqual(len(res.data), 1)
