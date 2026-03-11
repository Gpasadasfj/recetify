from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from recetify.services import register_user

from .forms import LoginForm, RegisterForm
from recipes.models import Recipe


class HomeView(ListView):
    model = Recipe
    template_name = "general/home.html"
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Recipe.objects.all()

        if self.request.user.is_authenticated:
            logged_profile = self.request.user.profile
            queryset = queryset.filter(
            user__profile__following_set__follower=logged_profile
            )

        search_filter = self.request.GET.get("search")
        fast_recipe = self.request.GET.get("max_time")
        easy_recipe = self.request.GET.get("difficulty")
        food_category = self.request.GET.get("food_category")


        if search_filter:
            queryset = queryset.filter(title__icontains=search_filter)

        if fast_recipe:
            queryset = queryset.filter(
                time__lte=timedelta(minutes=int(fast_recipe))
            )
            queryset = queryset.exclude(time__isnull=True)

        if easy_recipe:
            queryset = queryset.filter(difficulty__name__iexact="Fácil")

        if food_category:
            queryset = queryset.filter(food_category__name__iexact=food_category)


        return queryset.distinct()
    

class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.user)
        return redirect("home")


class RegisterView(CreateView):
    template_name = "general/register.html"
    form_class = RegisterForm
    model = User
    success_url = reverse_lazy("profiles:edit_profile")

    def form_valid(self, form):
        user = register_user(data=form.cleaned_data)

        login(self.request, user)
        messages.success(self.request, "Usuario creado correctamente.")

        return redirect(self.success_url)
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
