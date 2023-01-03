from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase


class BaseTest(APITestCase):
    def setUp(self) -> None:

        # define general urls
        self.login_web_path = reverse("users:login_web")

        # create users
        self.superuser = get_user_model().objects.create_user(
            username="jack",
            password="Jack1234",
            is_active=True,
            is_superuser=True,
        )
        self.superuser_data = {"username": "jack", "password": "Jack1234"}

        self.user1 = get_user_model().objects.create_user(
            username='david',
            password='David1234',
            is_active=True,
        )
        self.user1_data = {"username": "david", "password": "David1234"}

        self.user2 = get_user_model().objects.create_user(
            username='alice',
            password='Alice1234',
            is_active=True,
        )
        self.user2_data = {"username": "alice", "password": "Alice1234"}

        self.user3 = get_user_model().objects.create_user(
            username='peter',
            password='Peter1234',
            is_active=True,
        )
        self.user3_data = {"username": "peter", "password": "Peter1234"}

        self.user4 = get_user_model().objects.create_user(
            username='james',
            password='James1234',
            is_active=True,
        )
        self.user4_data = {"username": "james", "password": "James1234"}

        # login operations
        self.login_superuser_response = self.client.post(
            path=self.login_web_path,
            data=self.superuser_data,
        )
        self.superuser_access_token = self.login_superuser_response.data["access"]

        self.login_user1_response = self.client.post(
            path=self.login_web_path,
            data=self.user1_data
        )
        self.user1_access_token = self.login_user1_response.data["access"]

        self.login_user2_response = self.client.post(
            path=self.login_web_path,
            data=self.user2_data
        )
        self.user2_access_token = self.login_user2_response.data["access"]

        self.login_user3_response = self.client.post(
            path=self.login_web_path,
            data=self.user3_data
        )
        self.user3_access_token = self.login_user3_response.data["access"]

        self.login_user4_response = self.client.post(
            path=self.login_web_path,
            data=self.user4_data
        )
        self.user4_access_token = self.login_user4_response.data["access"]
