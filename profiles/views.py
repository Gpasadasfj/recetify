from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, View

from profiles.models import Follow
from profiles.services import toggle_follow, update_profile
from recipes.models import Recipe

from .forms import UserForm, UserProfileForm
from .models import UserProfile


@method_decorator(never_cache, name="dispatch")
class ProfilesListView(ListView):
    model = UserProfile
    template_name = "profiles/profiles_list.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
        else:
            user_profile = None

        following_ids = set(
            Follow.objects.filter(follower=user_profile)
            .values_list('following_id', flat=True)
        )
        context['following_ids'] = following_ids
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
    
        # --- Filtro por nombre ---
        search_filter = self.request.GET.get("search")
        if search_filter:
            queryset = queryset.filter(
                Q(user__username__icontains=search_filter) |
                Q(user__first_name__icontains=search_filter) |
                Q(user__last_name__icontains=search_filter)
            ).distinct()
            
        return queryset


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        if self.request.user.is_authenticated:
            context["following"] = Follow.objects.filter(
                follower=self.request.user.profile, following=profile
            ).exists()
        else:
            context["following"] = False

        context["followers_number"] = Follow.objects.filter(following=profile).count()
        context["following_number"] = Follow.objects.filter(follower=profile).count()

        if self.request.user.is_authenticated:
            context["saved_recipes"] = Recipe.objects.filter(
                saverecipe__user=self.request.user
            )
        else:
            context["saved_recipes"] = Recipe.objects.none()

        context["recipes"] = Recipe.objects.filter(user=profile.user)

        return context


class ToggleFollowView(View):  
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        following = get_object_or_404(UserProfile, pk=kwargs["pk"])
        follower = request.user.profile

        is_following = toggle_follow(follower, following)
        followers = Follow.objects.filter(following=following).count()

        return JsonResponse({"following": is_following, "followers": followers})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = "profiles/edit_profile.html"
    form_class = UserProfileForm
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        profile_form = self.get_form()
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            update_profile(profile_form, user_form)
            return redirect(self.get_success_url())

        context = self.get_context_data(form=profile_form)
        context["user_form"] = user_form
        return self.render_to_response(context)

    def get_success_url(self):
        profile_pk = self.request.user.pk
        return reverse("profiles:profile_detail", kwargs={"pk": profile_pk})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user

        if request.user != user:
            return HttpResponseForbidden()

        logout(request)
        user.delete()
        return redirect(self.success_url)
