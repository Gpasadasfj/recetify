from django.db import transaction

from profiles.models import Follow

@transaction.atomic
def toggle_follow(follower, following):
    if follower is None:
        raise ValueError("Follower is required")

    if follower.pk == following.pk:
        return False

    relation, created = Follow.objects.get_or_create(
        follower=follower, following=following
    )
    if not created:
        relation.delete()
        return False

    return True


@transaction.atomic
def update_profile(profile_form, user_form):
    profile_form.save(),
    user_form.save()
