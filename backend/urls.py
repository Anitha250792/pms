from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Allauth (Google login) — MUST COME BEFORE /user/
    path("accounts/", include("allauth.urls")),

    # Custom login/register/profile
    path("user/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # App URLs
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),
    path("communications/", include(("communications.urls", "communications"), namespace="communications")),

    # Redirect root → custom login page
    path("", lambda request: redirect("/user/login/")),
    path("design/", include("design.urls")),
    path("notifications/", include("notifications.urls")),
]

# Media files (dev only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
