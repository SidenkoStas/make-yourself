from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger-ui"),
    path("", include("common.urls", namespace="common")),
    path("api/v1/blog/", include("blog.api_urls", namespace="blog")),
    path("api/v1/account/", include("users.api_urls")),
    path("api/v1/skill_test/", include("skill_tests.api_urls", namespace="skill_test"))

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns.extend([
        path("__debug__/", include("debug_toolbar.urls"))])
