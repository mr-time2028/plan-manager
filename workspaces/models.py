from django.db import models
from django.contrib.auth import get_user_model


class Workspace(models.Model):
    team_members = models.ManyToManyField(get_user_model())
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskGroup(models.Model):
    title = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


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

    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    users = models.ManyToManyField(get_user_model())
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    expire_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
