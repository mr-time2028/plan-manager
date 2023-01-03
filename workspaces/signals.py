from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import (
    pre_save,
    post_delete,
)

from .models import (
    Board,
    Workspace,
    WorkspaceUser,
)


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


@receiver(pre_save, sender=Board)
@receiver(pre_save, sender=Workspace)
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_gen(instance, "title")


@receiver(post_delete, sender=WorkspaceUser)
def change_owner(sender, instance, *args, **kwargs):
    if instance.role == WorkspaceUser.OWNER and \
            not WorkspaceUser.objects.filter(
                Q(workspace__title=instance.workspace.title) & \
                Q(role=WorkspaceUser.OWNER)
            ).exists():
        oldest_member = WorkspaceUser.objects.filter(
            workspace__title=instance.workspace.title
        ).order_by("joined_at").first()
        if oldest_member:
            oldest_member.role = WorkspaceUser.OWNER
            oldest_member.save()
