from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        "Imagen de perfil", upload_to="profile_pictures/", blank=True, null=True
    )
    bio = models.TextField("Biografía", max_length=500, blank=True, null=True)
    birth_date = models.DateField("Fecha de nacimiento", blank=True, null=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", through="Follow"
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return self.user.username 

    def get_absolute_url(self):
        return reverse("profiles:profile_detail", args=[self.pk])

    @property
    def profile_image_url(self):
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        return static("img/default_profile.png")

    @property
    def full_name_title(self):
        return f"{self.user.first_name.title()} {self.user.last_name.title()}"


class Follow(models.Model):
    follower = models.ForeignKey(
        UserProfile,
        verbose_name="¿Quien sigue?",
        on_delete=models.CASCADE,
        related_name="follower_set",
    )
    following = models.ForeignKey(
        UserProfile,
        verbose_name="¿A quien sigue?",
        on_delete=models.CASCADE,
        related_name="following_set",
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="¿Desde cuando lo sigue?"
    )

    class Meta:
        verbose_name = "Seguidor"
        verbose_name_plural = "Seguidores"

        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            )
        ]

    def __str__(self):
        return f"{self.follower} sigue a {self.following}"
