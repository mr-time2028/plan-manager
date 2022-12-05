from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Workspace


def unique_slug_gen(instance, field, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field), allow_unicode=True)
    class_model = instance.__class__
    num = 1
    while class_model.objects.filter(slug=slug).exists():
        slug = f"{slug}-{num}"
        num += 1

    return slug


@receiver(pre_save, sender=Workspace)
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_gen(instance, "title")
