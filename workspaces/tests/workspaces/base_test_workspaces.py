from ..base_test import BaseTest
from workspaces.models import (
    Workspace,
    WorkspaceUser,
)


class BaseTestWorkspaces(BaseTest):
    def setUp(self) -> None:

        super().setUp()

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
