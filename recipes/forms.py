from datetime import timedelta
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import Ingredient, Rating, Recipe, Steps

class RecipeForm(forms.ModelForm):

    hours = forms.IntegerField(required=False, min_value=0, error_messages={
        "invalid": _("Introduce un número válido para las horas."),
    })
    minutes = forms.IntegerField(required=True, min_value=0, error_messages={
        "required": _("Indica los minutos de preparación."),
        "invalid": _("Introduce un número válido para los minutos.")
    })
    difficulty = forms.TextInput()
                                   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.time:
            total_minutes = int(self.instance.time.total_seconds() // 60)
            self.fields["hours"].initial = total_minutes // 60
            self.fields["minutes"].initial = total_minutes % 60

    class Meta:
        model = Recipe
        exclude = ["user", "created_at", "rating", "time"]
        error_messages = {
            "title": {
                "required": _("El título de la receta es obligatorio."),
                "max_length": _("El título no puede superar los 100 caracteres.")
            },
            "image": {
                "required": _("Debes subir una imagen para la receta."),
                "invalid": _("El archivo subido no es una imagen válida."),
            },
            "food_category": {
                "required": _("Selecciona al menos una categoría."),
            }
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "border-none w-full pt-4 border-none pl-4 pr-4 font-title font-bold text-2xl placeholder:text-gray-400 md:text-3xl focus:outline-none focus:ring-0",
                "placeholder": _("Nombre de la Receta")
            }),
            "description": forms.Textarea(attrs={
                "class": "border-none w-full pl-4 pr-4 pb-4 pt-0 font-primary text-s focus:outline-none focus:ring-0 placeholder:text-gray-400 focus:ring-0 md:text-lg",
                "rows": 2,
                "placeholder": _("Añade una breve descripción...")
            }),
            "food_category": forms.CheckboxSelectMultiple(attrs={"class": "hidden peer"})
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            max_size = 2 * 1024 * 1024  # 2MB
            if image.size > max_size:
                raise forms.ValidationError(_("La imagen no puede superar los 2MB."))
        return image

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title) < 3:
            raise forms.ValidationError(_("El título debe tener al menos 3 caracteres."))
        return title



    def clean(self):
        cleaned = super().clean()
        hours = int(cleaned.get("hours") or 0)
        minutes = int(cleaned.get("minutes") or 0)
        cleaned["time"] = timedelta(hours=hours, minutes=minutes)
        return cleaned


class StepForm(forms.ModelForm):
    class Meta:
        model = Steps
        fields = ["description"]
        error_messages = {
            "description": {
                "required": _("Cada paso debe tener una descripción.")
            }
        }
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": _("Describe el paso..."),
                "class": "rounded-2xl p-2 w-full border border-gray-300 shadow-md focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none"
            })
        }

class IngredientForm(forms.ModelForm):
        
    class Meta:
        model = Ingredient
        fields = ["quantity", "unit", "name"]
        error_messages = {
            "quantity": {
                "required": _("Introduce la cantidad del ingrediente."),
                "invalid": _("Introduce un número válido.")
            },
            "name": {
                "required": _("El ingrediente debe tener un nombre.")
            },
            "unit": {
                "required": _("Selecciona la unidad del ingrediente.")
            }
        }
        widgets = {
            "quantity": forms.NumberInput(attrs={
                "step": "0.5",
                "placeholder": _("10"),
                "class": "w-15 rounded-xl text-center border border-gray-300 font-bold text-gray-500 focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none placeholder:text-gray-400 md:w-20"
            }),
            "unit": forms.Select(attrs={"class": "hidden"}),
            "name": forms.TextInput(attrs={
                "placeholder": _("  Nombre del ingrediente"),
                "class": "rounded-xl w-full px-2 border border-gray-300 focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none placeholder:text-gray-400 md:max-w-[60dvw] md:w-[60dvw]"
            })
        }

StepFormSet = inlineformset_factory(
    Recipe,
    Steps,
    form=StepForm,
    extra=1,
    can_delete=True
)

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True,
)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
