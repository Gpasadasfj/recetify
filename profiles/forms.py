from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import UserProfile

BASE_CLASS = "w-full pl-10 py-2 mt-2 rounded-xl bg-(--bg-color) border border-gray-300 font-bold text-gray-500 focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none placeholder:text-gray-400"

BASE_CLASS_USER_PROFILE = "w-full cursor-pointer px-4 py-2 mt-2 rounded-xl bg-(--bg-color) border border-gray-300 font-bold text-gray-500 focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none placeholder:text-gray-400"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": BASE_CLASS
            }),
            "last_name": forms.TextInput(attrs={
                "class": BASE_CLASS
            }),
            "username": forms.TextInput(attrs={
                "class": BASE_CLASS
            }),
            "email": forms.EmailInput(attrs={
                "class": BASE_CLASS
            }),
        }


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={
            "invalid": _("La imagen seleccionada no es válida."),
            "invalid_image": _("El archivo subido no es una imagen válida o está dañado."),
        }
    )
        
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "bio", "birth_date"]
        widgets = {
            "birth_date": forms.DateInput(attrs={
                "type": "date",
                "class": BASE_CLASS_USER_PROFILE
            }),
            "bio": forms.Textarea(attrs={
                "class": BASE_CLASS_USER_PROFILE
            }),
        }