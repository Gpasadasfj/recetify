from django.urls import path

from .views import (
    DeleteRecipeView,
    RecipeCreateView,
    RecipeDetailView,
    RecipeListView,
    RecipeUpdateView,
    delete_step,
    save_recipe_ajax,
)

app_name = "recipes"

urlpatterns = [
    path("create/", RecipeCreateView.as_view(), name="create_recipe"),
    path("list/", RecipeListView.as_view(), name="recipe_list"),
    path("detail/<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("save/<int:pk>/", save_recipe_ajax, name="save_recipe"),
    path("update/<int:pk>/", RecipeUpdateView.as_view(), name="update_recipe"),
    path("delete/<int:pk>/", DeleteRecipeView.as_view(), name="delete_recipe"),
    path("step/delete/<int:pk>/", delete_step, name="delete_step"),
]
