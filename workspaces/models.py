from django.db import models
from django.contrib.auth import get_user_model


class Workspace(models.Model):
    members = models.ManyToManyField(get_user_model(), through='WorkspaceUser', related_name="workspace")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, allow_unicode=True, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WorkspaceUser(models.Model):
    OWNER = 'o'
    MEMBER = 'm'
    ROLE_CHOICES = (
        (OWNER, 'owner'),
        (MEMBER, 'member'),
    )
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="workspace_user")
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="workspace_user")
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='m')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['workspace', 'member'], name='unique workspace member')
        ]


class Board(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, allow_unicode=True, unique=True, blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="board")
    members = models.ManyToManyField(get_user_model(), through='BoardUser', related_name="board")

    def __str__(self):
        return self.title


class BoardUser(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="board_user")
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="board_user")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['board', 'member'], name='unique board member')
        ]


class Group(models.Model):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="group")

    def __str__(self):
        return self.title


class Task(models.Model):
    DONE = 'd'
    WORKING = 'w'
    STUCK = 's'
    UNKNOWN = 'u'
    STATUS_CHOICES = (
        (DONE, 'Done'),
        (WORKING, 'Working on it'),
        (STUCK, 'Stuck'),
        (UNKNOWN, 'Unknown')
    )

    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="task")
    users = models.ManyToManyField(get_user_model(), related_name="task")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    expire_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
