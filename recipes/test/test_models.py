from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase

from recipes.models import Category, Difficulty, Rating, Recipe, SaveRecipe, Steps


class CategoryModelTest(TestCase):

    def test_str_returns_name(self):
        category = Category.objects.create(name="Postres")
        self.assertEqual(str(category), "Postres")


class DifficultyModelTest(TestCase):

    def test_str_returns_name(self):
        difficulty = Difficulty.objects.create(name="Fácil")
        self.assertEqual(str(difficulty), "Fácil")


class RecipeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user1", password="1234")

    def test_str_returns_title(self):
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )
        self.assertEqual(str(self.recipe), "Test")

    def test_total_time_display_minutes_only(self):
        self.diff = Difficulty.objects.create(name="Fácil")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg"),
            time=timedelta(minutes=45)
        )

        self.assertEqual(self.recipe.time_data["display"], "45 min")

    def test_total_time_display_hours_and_minutes(self):
        self.diff = Difficulty.objects.create(name="Fácil")
        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Receta",
            difficulty=self.diff,
            description="Desc",
            time=timedelta(hours=2, minutes=30),
        )

        self.assertEqual(self.recipe.time_data["display"], "2h 30min")


class StepsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user1", password="1234")
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )

    def test_steps_are_ordered_by_order_field(self):
        step2 = Steps.objects.create(recipe=self.recipe, order=2, description="Segundo")
        step1 = Steps.objects.create(recipe=self.recipe, order=1, description="Primero")

        steps = list(self.recipe.steps.all())

        self.assertEqual(steps[0], step1)
        self.assertEqual(steps[1], step2)


class RatingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user1", password="1234")
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )

    def test_str_returns_user_recipe_and_value(self):
        rating = Rating.objects.create(user=self.user, recipe=self.recipe, value=8.5)

        self.assertEqual(str(rating), f"{self.user} -> {self.recipe} (8.5)")

    def test_user_can_rate_recipe_only_once(self):
        Rating.objects.create(user=self.user, recipe=self.recipe, value=7.0)

        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=self.user, recipe=self.recipe, value=8.0)


class SaveRecipeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user1", password="1234")
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")
        self.recipe = Recipe.objects.create(
            title="Test",
            user=self.user,
            difficulty=self.diff,
            image=SimpleUploadedFile(name="img.jpg", content=b"fake", content_type="image/jpeg")
        )

    def test_str_returns_user_and_recipe(self):
        saved = SaveRecipe.objects.create(user=self.user, recipe=self.recipe)

        self.assertEqual(str(saved), f"{self.user} guardó la receta: {self.recipe}")

    def test_user_cannot_save_same_recipe_twice(self):
        SaveRecipe.objects.create(user=self.user, recipe=self.recipe)

        with self.assertRaises(IntegrityError):
            SaveRecipe.objects.create(user=self.user, recipe=self.recipe)
