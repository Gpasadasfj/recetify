from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from profiles.models import UserProfile
from recipes.models import Category, Difficulty, Recipe, SaveRecipe


class RecipeCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("recipes:create_recipe")
        self.user = User.objects.create_user(username="test", password="1234")
        self.profile = UserProfile.objects.create(user=self.user)
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")

    def test_create_recipe_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_get_create_recipe_view_logged_in(self):
        self.client.login(username="test", password="1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("steps", response.context)
        self.assertIn("ingredients", response.context)

    @patch("django.forms.fields.ImageField.to_python")
    @patch("recipes.views.create_or_update_recipe")
    def test_post_valid_creates_recipe(self, mock_create_recipe, mock_image_to_python):
        self.client.login(username="test", password="1234")

        # Mockear la conversión de ImageField para que siempre devuelva un archivo válido
        mock_image_to_python.return_value = SimpleUploadedFile(
            "test.jpg", b"fakeimagecontent", content_type="image/jpeg"
        )

        # Mock del servicio que crea la receta, con pk para reverse
        mock_create_recipe.return_value = type('RecipeMock', (), {'pk': 1})()

        data = {
            "title": "Receta test",
            "description": "Desc",
            "hours": "0",
            "minutes": "30",
            "difficulty": self.diff.id,
            "food_category": [self.cat.id],
            

            "steps-TOTAL_FORMS": "1",
            "steps-INITIAL_FORMS": "0",
            "steps-MIN_NUM_FORMS": "0",
            "steps-MAX_NUM_FORMS": "1000",
            "steps-0-description": "Paso 1",
            "steps-0-order": "1",

            "ingredient-TOTAL_FORMS": "1",
            "ingredient-INITIAL_FORMS": "0",
            "ingredient-MIN_NUM_FORMS": "0",
            "ingredient-MAX_NUM_FORMS": "1000",
            "ingredient-0-name": "Ingrediente",
            "ingredient-0-quantity": "100",
            "ingredient-0-unit": "g",
        }

        response = self.client.post(self.url, data)

        self.assertTrue(mock_create_recipe.called)
        self.assertEqual(response.status_code, 302)


class RecipeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")
        self.diff_easy = Difficulty.objects.create(name="Fácil")
        self.diff_hard = Difficulty.objects.create(name="Difícil")
        self.cat_breakfast = Category.objects.create(name="Desayuno")
        self.cat_dinner = Category.objects.create(name="Cena")

        self.recipe_easy = Recipe.objects.create(
            title="Fast",
            time=timedelta(minutes=10),
            user=self.user,
            difficulty=self.diff_easy,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg"),
        )
        self.recipe_easy.food_category.add(self.cat_breakfast)

        self.recipe_hard = Recipe.objects.create(
            title="Slow",
            time=timedelta(minutes=40),
            user=self.user,
            difficulty=self.diff_hard,
            image=SimpleUploadedFile(name="img2.jpg", content=b"fake", content_type="image/jpeg"),
        )
        self.recipe_hard.food_category.add(self.cat_dinner)

        self.url = reverse("recipes:recipe_list")

    def test_list_returns_all(self):
        response = self.client.get(self.url)
        recipes = response.context["recipes"]
        self.assertEqual(recipes.count(), 2)

    def test_filter_by_time(self):
        response = self.client.get(self.url + "?time=2")
        recipes = response.context["recipes"]
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes.first().title, "Fast")

    def test_filter_by_difficulty(self):
        response = self.client.get(self.url + "?difficulty=easy")
        recipes = response.context["recipes"]
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes.first().difficulty.name, "Fácil")

    def test_filter_by_food_type(self):
        response = self.client.get(self.url + "?food_type=breakfast")
        recipes = response.context["recipes"]
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes.first().food_category.first().name, "Desayuno")

    def test_filter_by_search(self):
        response = self.client.get(self.url + "?search=fast")
        recipes = response.context["recipes"]
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes.first().title, "Fast")


class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")
        self.profile = UserProfile.objects.create(user=self.user)
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )
        self.recipe.food_category.add(self.cat)
        self.url = reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        self.saved = SaveRecipe.objects.create(user=self.user, recipe=self.recipe)

    def test_detail_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["rating_form"] is None)

    def test_detail_logged_in_user_context(self):
        self.client.login(username="test", password="1234")
        response = self.client.get(self.url)
        self.assertTrue(response.context["is_saved"])
        self.assertIsNotNone(response.context["rating_form"])


class RecipeUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="1234")
        self.profile = UserProfile.objects.create(user=self.user)
        self.other_user = User.objects.create_user(username="other", password="1234")
        self.other_profile = UserProfile.objects.create(user=self.other_user)
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Receta",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )
        self.recipe.food_category.add(self.cat)
        self.url = reverse("recipes:update_recipe", kwargs={"pk": self.recipe.pk})

    def test_redirect_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_redirect_if_not_owner(self):
        self.client.login(username="other", password="1234")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("home"))

    def test_owner_can_access(self):
        self.client.login(username="owner", password="1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("steps", response.context)