import json

from django.urls import reverse

from .base_test_workspaces import BaseTestWorkspaces
from ...models import Workspace


class WorkspaceTest(BaseTestWorkspaces):
    def test_all_workspaces(self):
        """
        just superuser can access to list of all workspaces
        """
        self.all_workspaces_path = reverse("workspaces:workspaces-all-workspaces")

        response1 = self.client.get(
            path=self.all_workspaces_path,
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}'
        )
        self.assertEqual(response1.status_code, 200)     # superuser can see all workspaces

        response2 = self.client.get(
            path=self.all_workspaces_path,
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
        )
        self.assertEqual(response2.status_code, 403)     # user1 is not superuser so cannot see all workspaces

    def test_user_workspaces(self):
        """
        each user can see workspaces that is a member of it
        """
        self.user_workspaces_path = reverse("workspaces:workspaces-user-workspaces")

        response1 = self.client.get(
            path=self.user_workspaces_path,
            HTTP_AUTHORIZATION= f'Bearer {self.user2_access_token}'
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(response1.data), 2)    # user2 is member of two workspace

    def test_retrieve_workspace(self):
        """
        each user can see workspace detail that is a part of it
        superuser can see all workspaces detail
        """
        response1 = self.client.get(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace2.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
        )
        self.assertEqual(response1.status_code, 403)    # user1 is not a part of workspace2, so cannot see detail of workspace2

        response2 = self.client.get(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
        )
        self.assertEqual(response2.status_code, 200)    # user1 is a part of workspace1, so can see detail of workspace1

        response3 = self.client.get(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace2.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
        )
        self.assertEqual(response3.status_code, 200)    # superuser can retrieve all workspaces

    def test_update_workspace(self):
        """
        each owner can update own workspaces
        """
        response1 = self.client.put(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
            data={"title": "new title"},
        )
        self.assertEqual(response1.status_code, 200)    # user1 is owner of workspace1, so can update workspace1
        self.assertEqual(json.loads(response1.content)["title"], "new title")

        response2 = self.client.put(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user2_access_token}',
            data={"title": "new title"},
        )
        self.assertEqual(response2.status_code, 403)    # user2 is a member of workspace1, so cannot update workspace1

        response3 = self.client.put(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user3_access_token}',
            data={"title": "new title"},
        )
        self.assertEqual(response3.status_code, 403)     # user3 is owner of workspace3, so cannot update workspace1 (although he/she is owner)

        response4 = self.client.put(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
            data={"title": "superuser changed title"},
        )
        self.assertEqual(response4.status_code, 200)     # superuser can update all workspaces
        self.assertEqual(json.loads(response4.content)["title"], "superuser changed title")

    def test_add_member(self):
        """
        each owner can add members to workspace (also superuser can do it), but members can't
        """
        response1 = self.client.post(
            path=reverse("workspaces:workspaces-add-member", kwargs={"slug": self.workspace1}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
            data={
                "members": {
                    self.user3.username: "owner",
                    self.user4.username: "member",
                },
            },
            format='json'
        )
        self.assertEqual(response1.status_code, 200)     # user1 is owner of workspace1, so can add member to workspace1

        response2 = self.client.post(
            path=reverse("workspaces:workspaces-add-member", kwargs={"slug": self.workspace2}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
            data={
                "members": {
                    self.user1.username: "owner",
                    self.user4.username: "member",
                }
            },
            format='json',
        )
        self.assertEqual(response2.status_code, 403)     # user1 is not owner of workspace2, so cannot add member to workspace2

        response3 = self.client.post(
            path=reverse("workspaces:workspaces-add-member", kwargs={"slug": self.workspace2}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
            data={
                "members": {
                    self.user1.username: "owner",
                    self.user4.username: "member",
                }
            },
            format='json',
        )
        self.assertEqual(response3.status_code, 200)     # superuser can add member to any workspace

        response4 = self.client.post(
            path=reverse("workspaces:workspaces-add-member", kwargs={"slug": self.workspace2}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
            data={
                "members": {
                    self.user1.username: "newRole",
                    self.user4.username: "member",
                }
            },
            format='json',
        )
        self.assertEqual(response4.status_code, 400)     # superuser can add member to any workspace

    def test_delete_workspace(self):
        """
        each owner can delete own workspaces
        """
        response1 = self.client.delete(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
        )
        self.assertEqual(response1.status_code, 200)     # user1 is owner of workspace1, so can delete workspace1
        with self.assertRaises(Workspace.DoesNotExist):
            Workspace.objects.get(slug=self.workspace1.slug)

        response2 = self.client.delete(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace2.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user3_access_token}',
        )
        self.assertEqual(response2.status_code, 403)     # user3 is a memjber of workspace2, so cannot delete workspace2 because he/she is not owner

        response3 = self.client.delete(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace3.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
        )
        self.assertEqual(response3.status_code, 403)     # user1 is owner of workspace1, so cannot delete workspace3 (although he/she is owner)

        response4 = self.client.delete(
            path=reverse("workspaces:workspaces-detail", kwargs={"slug": self.workspace2.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
        )
        self.assertEqual(response4.status_code, 200)     # superuser can delete all workspaces
        with self.assertRaises(Workspace.DoesNotExist):
            Workspace.objects.get(slug=self.workspace2.slug)

    def test_remove_member(self):
        """
        each owner cann remove members to workspace (also superuser can do it), but members can't
        """
        response1 = self.client.post(
            path=reverse("workspaces:workspaces-remove-member", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user1_access_token}',
            data={
                "members": {
                    self.user2.username: None,
                },
            },
            format="json",
        )
        self.assertEqual(response1.status_code, 200)      # user1 is owner of workspace1, so can remove members of workspace1

        response2 = self.client.post(
            path=reverse("workspaces:workspaces-remove-member", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.user2_access_token}',
            data={
                "members": {
                    self.user1.username: None,
                },
            },
            format="json",
        )
        self.assertEqual(response2.status_code, 403)      # user2 is a member of workspace1, so cannot remove members of workspace1

        response3 = self.client.post(
            path=reverse("workspaces:workspaces-remove-member", kwargs={"slug": self.workspace1.slug}),
            HTTP_AUTHORIZATION= f'Bearer {self.superuser_access_token}',
            data={
                "members": {
                    self.user2.username: None,
                },
            },
            format="json",
        )
        self.assertEqual(response3.status_code, 200)      # superuser can remove members from any workspace
