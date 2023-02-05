""" Test User List """
from django.test import (TestCase, Client)
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # create client
        self.client = Client()

        # create superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='testpass123')

        # force admin login
        self.client.force_login(self.admin_user)

        # create user
        self.user = get_user_model().objects.create(
            email='user@example.com', password='testpass123')

    def test_users_list(self):
        # get users url
        url = reverse('admin:core_user_changelist')

        # make call
        res = self.client.get(url)

        # make assertions
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user_page(self):
        # get users url
        url = reverse('admin:core_user_change', args=[self.user.id])

        # make call
        res = self.client.get(url)

        # make assertions
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        # get users url
        url = reverse('admin:core_user_add')

        # make call
        res = self.client.get(url)

        # make assertions
        self.assertEqual(res.status_code, 200)
