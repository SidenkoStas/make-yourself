from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls", namespace="common")),
    path("account/", include("users.urls", namespace="users")),
    # REST API
    path("api/v1/blog/", include("blog.api_urls", namespace="api_blog")),
    path("api/v1/account/", include("users.api_urls", namespace="api_users")),
    path("api/v1/skill_test/", include("skill_tests.api_urls", namespace="api_skill_test")),
    # OpenAPI docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns.extend([
        path("__debug__/", include("debug_toolbar.urls"))])
