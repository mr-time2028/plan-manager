from django.db import models
from django.contrib.auth import get_user_model


class Workspace(models.Model):
    members = models.ManyToManyField(get_user_model(), through='WorkspaceUser')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class WorkspaceUser(models.Model):
    OWNER = 'o'
    MEMBER = 'm'
    ROLE_CHOICES = (
        (OWNER, 'owner'),
        (MEMBER, 'member'),
    )
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)



class Board(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, allow_unicode=True, unique=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    members = models.ManyToManyField(get_user_model(), through='BoardUser')



class BoardUser(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)



class Group(models.Model):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)



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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    users = models.ManyToManyField(get_user_model())
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    expire_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
