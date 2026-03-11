from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from profiles.models import Follow

from .forms import RatingForm, RecipeForm, StepFormSet, IngredientFormSet
from .models import Difficulty, Rating, Recipe, SaveRecipe, Steps
from .services import (
    create_or_update_rating,
    create_or_update_recipe,
    delete_step_and_reorder,
    toggle_save_recipe,
)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/create_or_update_recipe.html"

    def get_success_url(self):
        return reverse("recipes:recipe_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["minutes"] = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        context["hours"] = [0, 1, 2, 3, 4, 5, 6, 7 , 8]
        context["difficulty"] = Difficulty.objects.all()
        
        if self.request.method == "POST":
            context["steps"] = StepFormSet(self.request.POST, prefix="steps")
            context["ingredients"] = IngredientFormSet(self.request.POST, prefix="ingredient")
        else:
            context["steps"] = StepFormSet(prefix="steps")
            context["ingredients"] = IngredientFormSet(prefix="ingredient")

        return context
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        context = self.get_context_data()
        steps_formset = context["steps"]
        ingredients_formset = context["ingredients"]

        if steps_formset.is_valid() and ingredients_formset.is_valid():
            self.object = create_or_update_recipe(
                recipe_form=form,
                steps_formset=steps_formset,
                ingredients_formset=ingredients_formset,
                user=self.request.user,
            )
            return redirect(self.get_success_url())

        return self.form_invalid(form)


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"

    def get_queryset(self):
        queryset = super().get_queryset()

        # --- Filtro por tiempo ---
        time_map = {
            "1": timedelta(minutes=5),
            "2": timedelta(minutes=15),
            "3": timedelta(minutes=30),
            "4": timedelta(hours=1),
            "5": timedelta(hours=2),
        }

        time_filter = self.request.GET.get("time")
        if time_filter in time_map:
            queryset = queryset.filter(time__lte=time_map[time_filter])

        # --- Filtro por dificultad ---
        difficulty_map = {
            "easy": "Fácil",
            "medium": "Medio",
            "hard": "Difícil",
        }

        difficulty_filter = self.request.GET.get("difficulty")
        if difficulty_filter in difficulty_map:
            queryset = queryset.filter(
                difficulty__name=difficulty_map[difficulty_filter]
            )

        # --- Filtro por tipo de comida ---
        food_type_map = {
            "breakfast": "Desayuno",
            "lunch": "Almuerzo",
            "dinner": "Cena",
            "snack": "Aperitivo",
            "pre-workout": "Preentreno",
            "post-workout": "Postentreno",
        }

        food_type_filters = self.request.GET.getlist("food_type")  # obtiene todos los seleccionados

        # Filtra solo los que están en el mapa
        selected_food_types = [food_type_map[v] for v in food_type_filters if v in food_type_map]

        if selected_food_types:
            queryset = queryset.filter(food_category__name__in=selected_food_types)

        search_filter = self.request.GET.get("search")

        # --- Filtro por nombre ---
        if search_filter:
            queryset = queryset.filter(title__icontains=search_filter)

        return queryset.distinct()


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # El usuario logeado sigue al creador de la receta?
        recipe = self.get_object()
        owner_profile = recipe.user.profile        # perfil del autor de la receta
        
        if self.request.user.is_authenticated:
            logged_profile = self.request.user.profile # perfil del usuario logueado    
            context["following"] = Follow.objects.filter(
                follower=logged_profile, following=owner_profile
            ).exists()
        else:
            context["following"] = False

        # ¿Ha valorado ya este usuario?
        if self.request.user.is_authenticated:
            rating = Rating.objects.filter(
                user=self.request.user, recipe=recipe
            ).first()
            context["rating_form"] = RatingForm(instance=rating)
        else:
            context["rating_form"] = None

        # Ha guardado ya la receta?
        if self.request.user.is_authenticated:
            is_saved = SaveRecipe.objects.filter(
                user=self.request.user, recipe=self.get_object()
            ).exists()

            context["is_saved"] = is_saved

        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            create_or_update_rating(request.user, self.get_object(), request.POST)

        return self.get(request, *args, **kwargs)


@login_required
def save_recipe_ajax(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_saved = toggle_save_recipe(recipe, request.user)

    return JsonResponse({"saved": is_saved})


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/create_or_update_recipe.html"

    def get_success_url(self):
        return reverse("recipes:recipe_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object().user
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["minutes"] = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        context["hours"] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        context["difficulty"] = Difficulty.objects.all()

        if self.request.method == "POST":
            context["steps"] = StepFormSet(
                self.request.POST,
                instance=self.object,
                prefix="steps",
            )
            context["ingredients"] = IngredientFormSet(
                self.request.POST,
                instance=self.object,
                prefix="ingredient",
            )
        else:
            context["steps"] = StepFormSet(
                instance=self.object,
                prefix="steps",
            )
            context["ingredients"] = IngredientFormSet(
                instance=self.object,
                prefix="ingredient",
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        steps_formset = context["steps"]
        ingredients_formset = context["ingredients"]

        if steps_formset.is_valid() and ingredients_formset.is_valid():
            create_or_update_recipe(
                recipe_form=form,
                steps_formset=steps_formset,
                ingredients_formset=ingredients_formset,
                recipe=self.object,
            )
            return redirect(self.get_success_url())

        return self.form_invalid(form)



@login_required
@require_POST
def delete_step(request, pk):
    step = get_object_or_404(Steps, pk=pk)

    # seguridad: solo el dueño
    if step.recipe.user != request.user:
        return JsonResponse({"success": False}, status=403)

    delete_step_and_reorder(step)
    return JsonResponse({"success": True})


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("home")

    def test_func(self):
        # Solo el dueño puede eliminar
        recipe = self.get_object()
        return self.request.user == recipe.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("home")