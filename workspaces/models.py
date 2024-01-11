from django.db import models


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
    slug = models.SlugField(blank=True, allow_unicode=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    expire_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
