# dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from accounts.models import CustomUser
from projects.models import Project
from tasks.models import Task
from communications.models import Message


# 🌍 Default dashboard redirect
@login_required
def dashboard(request):
    return redirect("dashboard:global_dashboard")


# 🌍 Global Overview (All users — Read-Only)
@login_required
def global_dashboard(request):
    projects = Project.objects.select_related("owner").all()

    latest = Message.objects.order_by("-created_at").first()
    announcements = [latest] if latest else []

    # 🔹 Chart data
    project_priority_data = (
        projects.values("priority")
        .annotate(count=Count("priority"))
        .order_by("priority")
    )

    task_status_data = (
        Task.objects.values("status")
        .annotate(count=Count("status"))
        .order_by("status")
    )

    show_role_hint = not getattr(request.user, "is_role_selected", False)

    context = {
        "projects": projects,
        "user_role": getattr(request.user, "role", None),
        "announcements": announcements,
        "show_role_hint": show_role_hint,
        "project_priority_data": list(project_priority_data),
        "task_status_data": list(task_status_data),
    }

    return render(request, "dashboard/global_dashboard.html", context)


# 🟥 HR Dashboard
@login_required
def hr_dashboard(request):
    if request.user.role != "HR":
        return render(request, "dashboard/403.html", {"message": "Unauthorized access"})

    context = {
        "total_projects": Project.objects.count(),
        "active_projects": Project.objects.exclude(status="Completed").count(),
        "total_tasks": Task.objects.count(),
        "total_members": CustomUser.objects.exclude(role="HR").count(),
        "messages": Message.objects.order_by("-created_at")[:50],
        "allow_edit": True,
    }

    return render(request, "dashboard/hr_dashboard.html", context)


# 🟦 Manager Dashboard
@login_required
def manager_dashboard(request):
    if request.user.role != "Manager":
        return render(request, "dashboard/403.html", {"message": "Unauthorized access"})

    user = request.user
    latest = Message.objects.order_by("-created_at").first()
    announcements = [latest] if latest else []

    projects = Project.objects.select_related("owner").all()
    tasks = Task.objects.all()

    project_priority_data = (
        projects.values("priority")
        .annotate(count=Count("priority"))
        .order_by("priority")
    )

    task_status_data = (
        tasks.values("status")
        .annotate(count=Count("status"))
        .order_by("status")
    )

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Completed").count()
    progress_percent = (completed_tasks / total_tasks * 100) if total_tasks else 0

    context = {
        "user": user,
        "user_role": "Manager",
        "projects": projects,
        "tasks": tasks,
        "projects_count": projects.count(),
        "tasks_count": tasks.count(),
        "project_priority_data": list(project_priority_data),
        "task_status_data": list(task_status_data),
        "progress_percent": round(progress_percent, 2),
        "team_summary": CustomUser.objects.filter(role="Team Member"),
        "pending_projects": Project.objects.none(),
        "announcements": announcements,
    }

    return render(request, "dashboard/manager_dashboard.html", context)


# 🟩 Member Dashboard
@login_required
def member_dashboard_view(request, user_id):
    member = get_object_or_404(CustomUser, id=user_id)

    if request.user != member and request.user.role != "Manager":
        return render(request, "dashboard/403.html", {"message": "Unauthorized access"})

    assigned_projects = Project.objects.filter(assigned_to=member)
    tasks = Task.objects.filter(assigned_to=member)

    project_priority_data = (
        assigned_projects.values("priority")
        .annotate(count=Count("priority"))
        .order_by("priority")
    )

    task_status_data = (
        tasks.values("status")
        .annotate(count=Count("status"))
        .order_by("status")
    )

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Completed").count()
    progress_percent = (completed_tasks / total_tasks * 100) if total_tasks else 0

    latest = Message.objects.order_by("-created_at").first()
    announcements = [latest] if latest else []

    context = {
        "member": member,
        "user_role": "Team Member",
        "projects": Project.objects.none(),
        "assigned_projects": assigned_projects,
        "tasks": tasks,
        "projects_count": assigned_projects.count(),
        "tasks_count": tasks.count(),
        "project_priority_data": list(project_priority_data),
        "task_status_data": list(task_status_data),
        "progress_percent": round(progress_percent, 2),
        "viewing_as_manager": request.user.role == "Manager" and request.user != member,
        "announcements": announcements,
        "user": request.user,
    }
    return render(request, "dashboard/member_dashboard.html", context)


# 🟪 Design Team Dashboard
@login_required
def design_dashboard(request):
    if request.user.role != "Design Team":
        return render(request, "dashboard/403.html", {"message": "Unauthorized access"})

    return render(request, "dashboard/design_dashboard.html", {"allow_edit": True})


# 🎯 Role Selection
@login_required
def select_role(request):
    user = request.user

    if request.method == "POST":
        selected_role = request.POST.get("role")

        if selected_role in ["HR", "Manager", "Team Member", "Design Team"]:
            user.role = selected_role
            user.is_role_selected = True
            user.save(update_fields=["role", "is_role_selected"])

            if selected_role == "HR":
                return redirect("dashboard:hr_dashboard")
            if selected_role == "Manager":
                return redirect("dashboard:manager_dashboard")
            if selected_role == "Team Member":
                return redirect("dashboard:member_dashboard", user.id)
            if selected_role == "Design Team":
                return redirect("dashboard:design_dashboard")

    return render(request, "dashboard/select_role.html")
