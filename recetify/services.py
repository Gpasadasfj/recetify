from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.db import transaction

@transaction.atomic
def register_user(data: dict) -> User:
    user = User(
        username=data["username"],
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"]
    )
    user.set_password(data["password"])
    user.save()

    UserProfile.objects.create(user=user)

    return user