from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseForbidden
from projects.models import Project
from .models import DesignUpload
from .forms import DesignUploadForm
from accounts.models import CustomUser
from notifications.utils import notify


@login_required
def design_dashboard(request):
    """
    Only Design Team can upload — others get read-only dashboard
    """
    projects = Project.objects.all().order_by("-created_at")
    uploads = DesignUpload.objects.all().order_by("-uploaded_at")

    return render(request, "design/dashboard.html", {
        "projects": projects,
        "uploads": uploads,
        "is_designer": request.user.role == "Design Team",  # fixed condition
    })


@login_required
def upload_design(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.role != "Design Team":
        return HttpResponseForbidden("You are not allowed to upload designs.")

    last_upload = DesignUpload.objects.filter(project=project).order_by("-version").first()
    next_version = (last_upload.version + 1) if last_upload else 1

    if request.method == "POST":
        form = DesignUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.project = project
            upload.uploaded_by = request.user
            upload.version = next_version
            upload.save()

            if project.assigned_to:
                notify(
                    user=project.assigned_to,
                    message=f"New design uploaded - {project.name} (v{upload.version})",
                    link=f"/design/{project.id}/detail/"
                )

                send_mail(
                    subject=f"New Design Uploaded for {project.name}",
                    message=f"A new design version {upload.version} was uploaded by {request.user.username}",
                    from_email="noreply@pms.com",
                    recipient_list=[project.assigned_to.email],
                    fail_silently=True,
                )

            messages.success(request, "🎨 Design uploaded successfully!")
            return redirect("design:design_detail", project_id=project.id)
    else:
        form = DesignUploadForm()

    return render(request, "design/upload_design.html", {
        "project": project,
        "form": form,
        "next_version": next_version,
    })


@login_required
def design_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    uploads = DesignUpload.objects.filter(project=project).order_by("-version")

    return render(request, "design/design_detail.html", {
        "project": project,
        "uploads": uploads,
    })
