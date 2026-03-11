from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


BASE_CLASS = "w-full pl-10 py-2 mt-2 rounded-xl bg-(--bg-color) border border-gray-300 font-bold text-gray-500 focus:border-(--primary-color) focus:ring focus:ring-(--primary-color) focus:outline-none placeholder:text-gray-400"

class LoginForm(forms.Form):

    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={
        "class": "rounded pl-4 bg-(--bg-color) border-gray-300 mt-2",
        "placeholder": "usuario_10"
    }))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        "class": "rounded pl-4 bg-(--bg-color) border-gray-300 mt-2",
        "placeholder": "*********"
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    "Usuario o contraseña incorrecto."
                )
            self.user = user

        return cleaned_data

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": BASE_CLASS, "placeholder": "********"}),
        error_messages={"required": "* Este campo es obligatorio."}
    )

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": BASE_CLASS, "placeholder": "********"}),
        error_messages={"required": "* Debes confirmar la contraseña."}
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    # 🔐 Validar que coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
             self.add_error(
                "password_confirm",
                "Las contraseñas no coinciden."
            )

        return cleaned_data

    # 🔒 Validar seguridad usando sistema oficial de Django
    def clean_password(self):
        password = self.cleaned_data.get("password")

        try:
            validate_password(password)
        except forms.ValidationError:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, "
                "no puede ser común ni completamente numérica.")

        return password

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.error_messages["required"] = "* Este campo es obligatorio."

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Juan",
                    "class": BASE_CLASS,
                },
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "García",
                    "class": BASE_CLASS,
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "juan_garcia10",
                    "class": BASE_CLASS,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "juan_garcia10@gmail.com",
                    "class": BASE_CLASS,
                }
            ),
        }
        error_messages = {
            "username": {
                "unique": "Este nombre de usuario ya está en uso.",
            },
            "email": {
                "invalid": "Introduce un correo electrónico válido.",
                "unique": "Este correo electrónico ya está en uso.",
            },
        }
