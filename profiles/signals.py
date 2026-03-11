import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_delete, sender=UserProfile)
def delete_userProfile_image(sender, instance, **kwargs):
    # Si el usuario tiene imagen la eliminamos
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)


@receiver(pre_save, sender=UserProfile)
def delete_old_userProfile_image(sender, instance, **kwargs):
    # Si el perfil tenia imagen la borramos
    if not instance.pk:
        return

    try:
        old_image = UserProfile.objects.get(pk=instance.pk).profile_picture
    except UserProfile.DoesNotExist:
        return

    new_image = instance.profile_picture

    # Comprobar que old_image tiene archivo real
    if old_image and hasattr(old_image, "path"):
        if not new_image or old_image.name != new_image.name:
            if os.path.exists(old_image.path):
                os.remove(old_image.path)
