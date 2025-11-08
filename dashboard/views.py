from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q
from accounts.models import CustomUser
from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):
    """
    Main Dashboard View:
      - Manager → full control & analytics view.
      - Team Member → sees only their created and assigned projects/tasks.
    """
    user = request.user
    user_role = getattr(user, "role", "Team Member")

    # ------------------------------------------
    # MANAGER DASHBOARD
    # ------------------------------------------
    if user_role == "Manager":
        projects = Project.objects.select_related("owner", "assigned_to").all()
        tasks = Task.objects.all()

        # 📊 Chart Data
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

        # ✅ Task completion stats
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="Completed").count()
        progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # 👥 Team summary (average completion per member)
        team_summary = (
            CustomUser.objects.filter(role="Team Member", assigned_projects__isnull=False)
            .annotate(avg_completion=Avg("assigned_projects__completion"))
            .distinct()
        )

        # 📘 Functional requirements list (static sample)
        functional_requirements = [
            {"id": "FR-01", "desc": "Allow CRUD for projects and tasks.", "priority": "High"},
            {"id": "FR-02", "desc": "Role-based access for Managers & Members.", "priority": "High"},
            {"id": "FR-03", "desc": "Analytics dashboard with charts.", "priority": "Medium"},
            {"id": "FR-04", "desc": "Track project and module progress.", "priority": "High"},
            {"id": "FR-05", "desc": "Real-time AJAX status updates.", "priority": "Medium"},
        ]

        context = {
            "user_role": "Manager",
            "projects": projects,
            "tasks": tasks,
            "projects_count": projects.count(),
            "tasks_count": tasks.count(),
            "project_priority_data": list(project_priority_data),
            "task_status_data": list(task_status_data),
            "progress_percent": round(progress_percent, 2),
            "functional_requirements": functional_requirements,
            "team_summary": team_summary,
        }

        return render(request, "dashboard/manager_dashboard.html", context)

    # ------------------------------------------
    # TEAM MEMBER DASHBOARD
    # ------------------------------------------
    else:
        # Projects the member created
        created_projects = Project.objects.filter(owner=user)
        # Projects assigned to them
        assigned_projects = Project.objects.filter(assigned_to=user)
        # Tasks assigned to them
        user_tasks = Task.objects.filter(assigned_to=user)

        # 📊 Chart Data
        project_priority_data = (
            (created_projects | assigned_projects)
            .values("priority")
            .annotate(count=Count("priority"))
            .order_by("priority")
        )

        task_status_data = (
            user_tasks.values("status")
            .annotate(count=Count("status"))
            .order_by("status")
        )

        # ✅ Completion progress
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(status="Completed").count()
        progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        context = {
            "user_role": "Team Member",
            "projects": created_projects,
            "assigned_projects": assigned_projects,
            "tasks": user_tasks,
            "projects_count": created_projects.count() + assigned_projects.count(),
            "tasks_count": user_tasks.count(),
            "project_priority_data": list(project_priority_data),
            "task_status_data": list(task_status_data),
            "progress_percent": round(progress_percent, 2),
            "member": user,
        }

        return render(request, "dashboard/member_dashboard.html", context)


# ==========================================================
# ✅ MANAGER VIEW — INDIVIDUAL TEAM MEMBER DASHBOARD
# ==========================================================
@login_required
def member_dashboard_view(request, user_id):
    """
    Manager can view an individual team member’s dashboard.
    Uses the same template as team members but data is filtered for that user.
    """
    member = get_object_or_404(CustomUser, id=user_id)

    # 🚫 Restrict access: only managers or the member themselves
    if request.user.role != "Manager" and request.user != member:
        return render(request, "403.html", {"message": "Access denied."})

    # Get the member's projects and tasks
    created_projects = Project.objects.filter(owner=member)
    assigned_projects = Project.objects.filter(assigned_to=member)
    tasks = Task.objects.filter(assigned_to=member)

    # 📊 Chart Data
    project_priority_data = (
        (created_projects | assigned_projects)
        .values("priority")
        .annotate(count=Count("priority"))
        .order_by("priority")
    )

    task_status_data = (
        tasks.values("status")
        .annotate(count=Count("status"))
        .order_by("status")
    )

    # ✅ Completion progress
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Completed").count()
    progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        "member": member,
        "user_role": "Team Member",
        "projects": created_projects,
        "assigned_projects": assigned_projects,
        "tasks": tasks,
        "projects_count": created_projects.count() + assigned_projects.count(),
        "tasks_count": tasks.count(),
        "project_priority_data": list(project_priority_data),
        "task_status_data": list(task_status_data),
        "progress_percent": round(progress_percent, 2),
        "viewing_as_manager": True,  # 👈 Helps show a "Back to Manager Dashboard" button
    }

    return render(request, "dashboard/member_dashboard.html", context)
