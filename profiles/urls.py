from django.urls import path

from .views import (
    ProfileDeleteView,
    ProfileDetailView,
    ProfilesListView,
    ProfileUpdateView,
    ToggleFollowView,
)

app_name = "profiles"

urlpatterns = [
    path("list/", ProfilesListView.as_view(), name="profiles_list"),
    path("detail/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("edit/", ProfileUpdateView.as_view(), name="edit_profile"),
    path("delete/<int:pk>/", ProfileDeleteView.as_view(), name="delete_profile"),
    path("toggle_follow/<int:pk>", ToggleFollowView.as_view(), name="toggle_follow"),
]
