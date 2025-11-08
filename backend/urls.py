from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Dashboard
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Project management
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),

    # Tasks
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),

    # Redirect root → login
    path("", lambda request: redirect("accounts:login")),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Optional error handlers
handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
