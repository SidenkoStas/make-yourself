from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger-ui"),
    path("", include("common.urls", namespace="common")),
    path("blog/", include("blog.urls", namespace="blog")),
    # path("users/", include("users.urls")),
    path("users/", include("dj_rest_auth.urls")),
    path("users/registration/", include("dj_rest_auth.registration.urls")),
    re_path(r"^account-confirm-email/(?P<key>[-:\w]+)/$",
            TemplateView.as_view(template_name="users/test.html"), name="account_confirm_email"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns.extend([
        path("__debug__/", include("debug_toolbar.urls"))])
