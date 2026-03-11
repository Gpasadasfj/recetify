from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from recipes.models import Difficulty, Recipe, SaveRecipe

from ..models import Follow, UserProfile
from ..services import toggle_follow


class ProfileListViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("profiles:profiles_list"))

    def test_profiles_list_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_profiles_in_context(self):
        self.assertIn("profiles", self.response.context)


class ProfileDetailViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="user1")
        self.user2 = User.objects.create_user(username="user2", password="user2")

        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

        self.url = reverse("profiles:profile_detail", args=[self.profile2.pk])

    def test_profile_detail_returns_200(self):
        self.client.login(username="user1", password="user1")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_following_is_true_or_false(self):
        response = self.client.get(self.url)
        self.assertFalse(response.context["following"])

        self.client.login(username="user1", password="user1")

        toggle_follow(self.profile1, self.profile2)
        response = self.client.get(self.url)

        self.assertTrue(response.context["following"])

    def test_followers_count_is_updated_after_follow(self):
        self.client.login(username="user1", password="user1")

        response = self.client.get(self.url)
        self.assertEqual(response.context["followers_number"], 0)

        toggle_follow(self.profile1, self.profile2)
        response = self.client.get(self.url)

        self.assertEqual(response.context["followers_number"], 1)

    def test_only_profile_recipes_are_in_context(self):
        # Creamos una dificultad para las recetas
        difficulty = Difficulty.objects.create(name="Fácil")

        # Imagen de prueba
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"",  # contenido vacío, suficiente para test
            content_type="image/jpeg"
        )

        # Creamos receta del perfil que estamos probando
        recipe1 = Recipe.objects.create(
            user=self.user2,
            title="Receta perfil",
            description="Descripción de la receta",
            difficulty=difficulty,
            image=image_file,
        )

        # Creamos receta de otro usuario que NO debe aparecer en el contexto
        recipe2 = Recipe.objects.create(
            user=self.user1,
            title="Receta otro usuario",
            description="Descripción de la receta",
            difficulty=difficulty,
            image=image_file,
        )

        self.client.login(username="user2", password="user2")
        response = self.client.get(self.url)

        recipes = response.context["recipes"]

        self.assertIn(recipe1, recipes)
        self.assertNotIn(recipe2, recipes)


class ToggleFollowViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="user1")
        self.user2 = User.objects.create_user("user2", password="user2")

        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

        self.url = reverse("profiles:toggle_follow", args=[self.profile2.pk])

    def test_toggle_follow_creates_follow(self):
        self.client.login(username="user1", password="user1")

        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Follow.objects.filter(
                follower=self.profile1, following=self.profile2
            ).exists()
        )

    def test_toggle_follow_returns_followers_count(self):
        self.client.login(username="user1", password="user1")

        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.json()["followers"], 1)

    def test_anonymous_user_cannot_toggle_follow(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Follow.objects.exists())

    def test_toggle_follow_removes_follow_if_exists(self):
        self.client.login(username="user1", password="user1")

        # Follow
        self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        # Unfollow
        self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertFalse(
            Follow.objects.filter(
                follower=self.profile1, following=self.profile2
            ).exists()
        )


class ProfileUpdateViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("profiles:edit_profile"))

        self.user1 = User.objects.create_user("user1", password="user1")
        self.user2 = User.objects.create_user("user2", password="user2")

        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_update_profile_requires_login(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertIn("/login/", self.response.url)

    def test_update_profile_get_returns_200_for_authenticated_user(self):
        self.client.login(username="user1", password="user1")

        response = self.client.get(reverse("profiles:edit_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("profile", response.context)
        self.assertIn("user_form", response.context)

    @patch("profiles.views.update_profile")
    def test_update_profile_redirects(self, mock_update_profile):
        self.client.login(username="user1", password="user1")

        response = self.client.post(
            reverse("profiles:edit_profile"),
            data={
                "bio": "Nueva bio",
                "birth_date": "2000-01-01",
                "first_name": "Nuevo",
                "last_name": "Nombre",
                "email": "nuevo@email.com",
                "username": "nuevonombre",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("profiles:profile_detail", kwargs={"pk": self.user1.pk})
        )
        mock_update_profile.assert_called_once()

    def test_update_profile_invalid_form_rerenders_page(self):
        self.client.login(username="user1", password="user1")

        response = self.client.post(
            reverse("profiles:edit_profile"), data={"email": "no-es-un-email"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["user_form"], "email", "Enter a valid email address."
        )


class MyProfileViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="user1")
        self.user2 = User.objects.create_user(username="user2", password="user2")

        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

        self.url = reverse("profiles:profile_detail", kwargs={"pk": self.user1.pk})

    def test_my_profile_returns_200_for_authenticated_user(self):
        self.client.login(username="user1", password="user1")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_my_profile_contains_only_saved_recipes(self):
        # Creamos una dificultad para las recetas
        difficulty = Difficulty.objects.create(name="Fácil")

        # Imagen de prueba
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"",  # contenido vacío, suficiente para test
            content_type="image/jpeg"
        )

        # Creamos receta del perfil que estamos probando
        recipe1 = Recipe.objects.create(
            user=self.user2,
            title="Receta perfil",
            description="Descripción de la receta",
            difficulty=difficulty,
            image=image_file,
        )

        # Creamos receta de otro usuario que NO debe aparecer en el contexto
        recipe2 = Recipe.objects.create(
            user=self.user1,
            title="Receta otro usuario",
            description="Descripción de la receta",
            difficulty=difficulty,
            image=image_file,
        )

        SaveRecipe.objects.create(user=self.user1, recipe=recipe1)

        self.client.login(username="user1", password="user1")

        response = self.client.get(self.url)

        saved_recipes = response.context["saved_recipes"]

        self.assertIn(recipe1, saved_recipes)
        self.assertNotIn(recipe2, saved_recipes)


class ProfileDeleteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="user1")
        self.profile = UserProfile.objects.create(user=self.user)

        self.url = reverse("profiles:delete_profile", args=[self.profile.pk])

    def test_delete_profile_requires_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_delete_profile_deletes_user_and_profile(self):
        self.client.login(username="user1", password="user1")

        response = self.client.post(self.url)

        self.assertRedirects(response, reverse("home"))

        self.assertFalse(User.objects.filter(username="user1").exists())
        self.assertFalse(UserProfile.objects.filter(pk=self.profile.pk).exists())

    def test_user_is_logged_out_after_profile_delete(self):
        self.client.login(username="user1", password="user1")

        self.client.post(self.url)

        self.assertNotIn("_auth_user_id", self.client.session)

    def test_user_cannot_delete_other_profile(self):
        other_user = User.objects.create_user(username="user2", password="user2")
        other_profile = UserProfile.objects.create(user=other_user)

        self.client.login(username="user1", password="user1")

        response = self.client.post(
            reverse("profiles:delete_profile", args=[other_profile.pk])
        )

        self.assertEqual(response.status_code, 403)
