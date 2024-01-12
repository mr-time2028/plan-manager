from django.db import models


class Task(models.Model):
    DONE = 'd'
    WORKING = 'w'
    UNFINISHED = 'u'
    STATUS_CHOICES = (
        (DONE, 'Done'),
        (WORKING, 'Working on it'),
        (UNFINISHED, "Unfinished"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=WORKING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
