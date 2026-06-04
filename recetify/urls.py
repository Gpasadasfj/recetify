from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import HomeView, LoginView, RegisterView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")), # Incluir la vista "set_language"
    ]

urlpatterns += (
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recipes/", include("recipes.urls")),
    path("profiles/", include("profiles.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("rosetta/", include("rosetta.urls"))
    ]