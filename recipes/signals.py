import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=Recipe)
def delete_old_recipe_image(sender, instance, **kwargs):
    if not instance.pk:
        return  # receta nueva, no hay imagen antigua

    try:
        old_image = Recipe.objects.get(pk=instance.pk).image
    except Recipe.DoesNotExist:
        return

    new_image = instance.image

    if old_image and old_image != new_image:
        if old_image.path and os.path.exists(old_image.path):
            os.remove(old_image.path)
