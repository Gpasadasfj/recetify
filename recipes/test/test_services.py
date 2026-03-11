from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from recipes.models import Recipe, Steps, Rating, SaveRecipe, Difficulty, Category
from recipes.forms import IngredientFormSet, RecipeForm, StepFormSet
from recipes.services import (
    create_or_update_recipe,
    create_or_update_rating,
    toggle_save_recipe,
    delete_step_and_reorder,
)


class ServicesTestCase(TestCase):

    def setUp(self):
        # Usuarios
        self.user = User.objects.create_user(username="user1", password="1234")
        self.other_user = User.objects.create_user(username="user2", password="1234")

        # Difficulty y Category
        self.diff = Difficulty.objects.create(name="Fácil")
        self.cat = Category.objects.create(name="Desayuno")

        # Recipe base
        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Receta 1",
            difficulty=self.diff,
            image=SimpleUploadedFile("img.jpg", b"fake", content_type="image/jpeg"),
            time=timedelta(minutes=10),
        )
        self.recipe.food_category.add(self.cat)

    @patch("django.forms.fields.ImageField.to_python")
    def test_create_or_update_recipe_create(self, mock_to_python):
        # Mockear ImageField para que siempre devuelva un archivo válido
        mock_to_python.return_value = SimpleUploadedFile(
            "test.jpg", b"fakeimagecontent", content_type="image/jpeg"
        )

        recipe_data = {
            "title": "Receta nueva",
            "description": "Descripción",
            "difficulty": self.diff.id,
            "hours": "0",
            "minutes": "20",
            "food_category": [self.cat.id],
            "image": mock_to_python.return_value,
        }

        recipe_form = RecipeForm(data=recipe_data, files={"image": mock_to_python.return_value})
        step_data = {
            "steps-TOTAL_FORMS": "1",
            "steps-INITIAL_FORMS": "0",
            "steps-MIN_NUM_FORMS": "0",
            "steps-MAX_NUM_FORMS": "1000",
            "steps-0-description": "Paso 1",
        }
        ingredient_data = {
            "ingredient-TOTAL_FORMS": "1",
            "ingredient-INITIAL_FORMS": "0",
            "ingredient-MIN_NUM_FORMS": "0",
            "ingredient-MAX_NUM_FORMS": "1000",
            "ingredient-0-name": "Ingrediente",
            "ingredient-0-quantity": "100",
            "ingredient-0-unit": "g",
        }

        step_formset = StepFormSet(step_data, instance=None, prefix="steps")
        ingredient_formset = IngredientFormSet(ingredient_data, instance=None, prefix="ingredient")

        # Verificar forms antes de assert
        if not recipe_form.is_valid():
            print("RecipeForm errors:", recipe_form.errors)

        if not step_formset.is_valid():
            print("StepFormSet errors:", step_formset.errors)

        if not ingredient_formset.is_valid():
            print("IngredientFormSet errors:", ingredient_formset.errors)

        # Asserts
        self.assertTrue(recipe_form.is_valid())
        self.assertTrue(step_formset.is_valid())
        self.assertTrue(ingredient_formset.is_valid())

        recipe = create_or_update_recipe(
            recipe_form=recipe_form,
            steps_formset=step_formset,
            ingredients_formset=ingredient_formset,
            user=self.user,
        )

        self.assertEqual(recipe.title, "Receta nueva")
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.steps.count(), 1)
        self.assertEqual(recipe.ingredient.count(), 1)

    def test_create_or_update_rating_create_and_update(self):
        data = {"value": 5.0}
        create_or_update_rating(self.user, self.recipe, data)
        rating = Rating.objects.get(user=self.user, recipe=self.recipe)
        self.assertEqual(rating.value, 5.0)

        # Actualizar
        data_update = {"value": 7.5}
        create_or_update_rating(self.user, self.recipe, data_update)
        rating.refresh_from_db()
        self.assertEqual(rating.value, 7.5)

    def test_toggle_save_recipe(self):
        # Guardar
        saved = toggle_save_recipe(self.recipe, self.user)
        self.assertTrue(saved)
        self.assertTrue(SaveRecipe.objects.filter(user=self.user, recipe=self.recipe).exists())

        # Eliminar
        unsaved = toggle_save_recipe(self.recipe, self.user)
        self.assertFalse(unsaved)
        self.assertFalse(SaveRecipe.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_delete_step_and_reorder(self):
        # Crear pasos
        step1 = Steps.objects.create(recipe=self.recipe, order=1, description="Paso 1")
        step2 = Steps.objects.create(recipe=self.recipe, order=2, description="Paso 2")
        step3 = Steps.objects.create(recipe=self.recipe, order=3, description="Paso 3")

        # Eliminar step2
        delete_step_and_reorder(step2)

        self.assertFalse(Steps.objects.filter(pk=step2.pk).exists())
        steps = self.recipe.steps.all().order_by("order")
        self.assertEqual(list(steps), [step1, step3])
        self.assertEqual(steps[0].order, 1)
        self.assertEqual(steps[1].order, 2)