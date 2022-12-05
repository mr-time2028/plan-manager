from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from workspaces.models import (
    Workspace,
    WorkspaceUser,
)


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

        # workspace1 -> members: user1(owner), user2
        self.workspace1 = Workspace.objects.create(title="workspace1")
        self.workspace1.members.add(self.user2)        # add members to workspace1
        self.workspace1_owner = WorkspaceUser.objects.create(
            workspace=self.workspace1,
            member=self.user1,
            role='o'
        )

        # workspace2 -> members: user2(owner), user3
        self.workspace2 = Workspace.objects.create(title="workspace2")
        self.workspace2.members.add(self.user3)        # add members to workspace2
        self.workspace2_owner = WorkspaceUser.objects.create(
            workspace=self.workspace2,
            member=self.user2,
            role='o'
        )

        # workspace3 -> members: user3(owner), user4
        self.workspace3 = Workspace.objects.create(title="workspace3")
        self.workspace3.members.add(self.user4)        # add members to workspace2
        self.workspace3_owner = WorkspaceUser.objects.create(
            workspace=self.workspace3,
            member=self.user3,
            role='o'
        )

        return super().setUp()
