from django.test import TestCase
# Defaul django user model NOTE: We can customize it
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email is successfull"""
        email = 'test@test.com'
        password = 'test1234'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        """An email for a new user is normalized"""
        email = 'test@TEST.COM'
        user = get_user_model().objects .create_user(
            email=email,
            password='123'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """creating test user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
