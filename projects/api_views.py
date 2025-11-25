from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def project_api(request, pk):
    """
    Returns full project data for modal display
    """
    project = get_object_or_404(Project, pk=pk)

    return JsonResponse({
        "id": project.id,
        "name": project.name,
        "description": project.description or "",
        "status": project.status,
        "priority": project.priority,
        "completion": project.completion,
        "progress_color": project.get_progress_color(),
        "assigned_to": project.assigned_to.username if project.assigned_to else None,
        "manager": project.owner.username if project.owner else None,
        "live_link": project.live_link,
        "assigned_date": project.assigned_date.strftime("%Y-%m-%d") if project.assigned_date else None,
        "delivery_date": project.delivery_date.strftime("%Y-%m-%d") if project.delivery_date else None,
    })
