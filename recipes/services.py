from django.db import transaction

from recipes.forms import RatingForm
from recipes.models import Rating, SaveRecipe


@transaction.atomic
def create_or_update_recipe(
    *,
    recipe_form,
    steps_formset,
    ingredients_formset,
    user=None,
    recipe=None,
):

    is_create = recipe is None

    # 1. Guardar receta
    recipe = recipe_form.save(commit=False)

    if is_create:
        recipe.user = user

    recipe.time = recipe_form.cleaned_data["time"]

    recipe.save()

    # M2M
    recipe.food_category.set(recipe_form.cleaned_data["food_category"])

    # 2. Pasos
    steps_formset.instance = recipe

    # Guardar los pasos válidos y eliminar los marcados DELETE
    order = 1
    for form in steps_formset.forms:
        # ignorar los que fueron marcados DELETE
        if form.cleaned_data.get('DELETE'):
            if form.instance.pk:
                form.instance.delete()  # eliminar de la DB
            continue

        description = form.cleaned_data.get('description', '').strip()
        if not description:
            # ignorar pasos vacíos
            if form.instance.pk:
                form.instance.delete()
            continue

        step = form.save(commit=False)
        step.recipe = recipe
        step.order = order  # asignamos el order correcto
        step.save()
        order += 1

    # 3. Ingredientes
    ingredients_formset.instance = recipe
    ingredients_formset.save()

    return recipe


def create_or_update_rating(user, recipe, data):
    rating = Rating.objects.filter(user=user, recipe=recipe).first()

    form = RatingForm(data, instance=rating)
    if form.is_valid():
        rating = form.save(commit=False)
        rating.user = user
        rating.recipe = recipe
        rating.save()


def toggle_save_recipe(recipe, user):
    saved = SaveRecipe.objects.filter(user=user, recipe=recipe)

    if saved.exists():
        saved.delete()
        return False
    else:
        SaveRecipe.objects.create(user=user, recipe=recipe)
        return True


@transaction.atomic
def delete_step_and_reorder(step):
    recipe = step.recipe
    step.delete()

    for index, s in enumerate(recipe.steps.all(), start=1):
        s.order = index
        s.save(update_fields=["order"])
