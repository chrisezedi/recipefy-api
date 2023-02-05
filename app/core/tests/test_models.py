""" Tests for models """
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_successful_superuser_creation(self):
        """create a superuser"""
        # create email and password values
        email = "testuser@example.com"
        password = "testpass123"

         # create user object
        user = get_user_model().objects.create_superuser(email=email, password=password)

        #assertions
        self.assertTrue(user.is_superuser,True)
        self.assertTrue(user.is_staff,True)

    def test_successful_user_creation(self):
        # create email and password values
        email = "testuser@example.com"
        password = "testpass123"

        # create user object
        user = get_user_model().objects.create_user(email=email, password=password)

        # assertions
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        #create sample emails
        sample_emails = {
            'test1@EXAMPLE.com':'test1@example.com',
            'Test2@Example.com':'Test2@example.com',
            'TEST3@EXAMPLE.com': 'TEST3@example.com',
            'test4@example.COM': 'test4@example.com'
            }

        for email in sample_emails:
            user = get_user_model().objects.create_user(email,'password123')
            self.assertEqual(user.email,sample_emails[email])