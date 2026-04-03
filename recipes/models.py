from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg



class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tipo de comida")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Difficulty(models.Model):
    name = models.CharField(max_length=10, verbose_name="Dificultad")

    class Meta:
        verbose_name = "Dificultad"
        verbose_name_plural = "Dificultades"

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe")
    title = models.CharField(max_length=200, verbose_name="Nombre de la receta")
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Foto de la receta",
    )
    food_category = models.ManyToManyField(Category, verbose_name="Tipo de comida")
    description = models.TextField(
        max_length=1000, default="", verbose_name="Descripción de la receta"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Fecha de creación")
    difficulty = models.ForeignKey(Difficulty, verbose_name="Dificultad", on_delete=models.CASCADE)
    time = models.DurationField(default=timedelta(minutes=0))

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ["created_at"]

    def __str__(self):
        return self.title

    @property
    def time_data(self):
        total_seconds = int(self.time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60

        return {
            "hours": hours,
            "minutes": minutes,
            "display": (
                f"{hours}h {minutes}min" if hours else f"{minutes} min"
            ),
        }

    def average_rating(self):
        result = self.ratings.aggregate(avg=Avg('value'))
        return result['avg'] or 0  # devuelve 0 si no hay valoraciones
    
    @property
    def full_name_title(self):
        return self.title.title()


class Ingredient(models.Model):

    class Unit(models.TextChoices):
        NONE = "-", "-" 
        GRAM = "g", "g"
        KILOGRAM = "kg", "kg"
        MILLILITER = "ml", "ml"
        LITER = "L", "L"
        UNIT = "", "uds"
        TABLESPOON = "cda", "cda"
        TEASPOON = "cdta", "cdta"

    name = models.CharField(max_length=50, verbose_name="Ingrediente")
    recipe = models.ForeignKey(Recipe , verbose_name="Receta", related_name="ingredient",  on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.NONE,
        verbose_name="Unidad"
    )

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        if self.quantity and self.unit:
            return f"{self.quantity} {self.get_unit_display()} de {self.name}"
        return self.name
    

class Steps(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveBigIntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Paso"
        verbose_name_plural = "Pasos"
        ordering = ["order"]

    def __str__(self):
        return f"Paso {self.order} de {self.recipe.title}"


class Rating(models.Model):
    RATINGS = [
        (0.5, "0.5"), 
        (1.0, "1"),
        (1.5, "1.5"),
        (2.0, "2"),
        (2.5, "2.5"),
        (3.0, "3"),
        (3.5, "3.5"),
        (4.0, "4"),
        (4.5, "4.5"),
        (5.0, "5"),
        (5.5, "5.5"),
        (6.0, "6"),
        (6.5, "6.5"),
        (7.0, "7"),
        (7.5, "7.5"),
        (8.0, "8"),
        (8.5, "8.5"),
        (9.0, "9"),
        (9.5, "9.5"),
        (10.0, "10"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    value = models.FloatField(choices=RATINGS)

    class Meta:
        unique_together = ["user", "recipe"]

    def __str__(self):
        return f"{self.user} -> {self.recipe} ({self.value})"

class SaveRecipe(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name="Receta", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="saved_recipe")
        ]

        verbose_name = "Receta guardada"
        verbose_name_plural = "Recetas guardadas"

    def __str__(self):
        return f"{self.user} guardó la receta: {self.recipe}"
