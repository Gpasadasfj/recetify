from django.contrib import admin

from .models import Category, Difficulty, Recipe, SaveRecipe, Steps


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Steps)
class StepsAdmin(admin.ModelAdmin):
    list_display = ["recipe", "order"]


@admin.register(SaveRecipe)
class SaveRecipeAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe"]


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ["name"]
