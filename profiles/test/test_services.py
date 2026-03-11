from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from profiles.forms import UserForm, UserProfileForm
from profiles.models import Follow, UserProfile
from profiles.services import toggle_follow, update_profile


class ToggleFollowServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")
        self.user2 = User.objects.create_user(username="test2", password="1234")

        self.profile = UserProfile.objects.create(user=self.user)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_anonymous_user_cannot_follow(self):
        with self.assertRaises(ValueError):
            toggle_follow(follower=None, following=self.profile2)

    def test_user_follows_other_user(self):
        is_following = toggle_follow(self.profile, self.profile2)

        self.assertTrue(is_following)
        self.assertEqual(Follow.objects.count(), 1)

    def test_user_cannot_follow_himself(self):
        is_following = toggle_follow(self.profile, self.profile)

        self.assertFalse(is_following)
        self.assertEqual(Follow.objects.count(), 0)

    def test_user_unfollow(self):
        is_following = toggle_follow(self.profile, self.profile2)
        new_is_following = toggle_follow(self.profile, self.profile2)

        self.assertTrue(is_following)
        self.assertFalse(new_is_following)
        self.assertEqual(Follow.objects.count(), 0)


class UpdateProfileServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="1234",
            first_name="Old",
            last_name="Name",
            email="old@email.com",
        )
        self.profile = UserProfile.objects.create(
            user=self.user, bio="Bio", birth_date=date(1990, 1, 1)
        )

        self.profile_form_data = {"bio": "Nueva bio", "birth_date": "2000-01-01"}
        self.user_form_data = {
            "first_name": "Nuevo",
            "last_name": "Nombre",
            "email": "nuevo@email.com",
            "username": "user1",
        }

    def test_update_profile_saves_changes(self):
        # Crear forms
        profile_form = UserProfileForm(self.profile_form_data, instance=self.profile)
        user_form = UserForm(self.user_form_data, instance=self.user)

        self.assertTrue(profile_form.is_valid())
        self.assertTrue(user_form.is_valid())

        # Llamar al service
        update_profile(profile_form, user_form)

        # Refrescar datos de la BD
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        # Comprobar cambios
        self.assertEqual(self.profile.bio, "Nueva bio")
        self.assertEqual(self.profile.birth_date, date(2000, 1, 1))
        self.assertEqual(self.user.first_name, "Nuevo")
        self.assertEqual(self.user.last_name, "Nombre")
        self.assertEqual(self.user.email, "nuevo@email.com")
