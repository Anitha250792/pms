from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import chain
from tasks.models import Task
from .models import Project, ProjectImage
from .forms import ProjectForm, ProjectImageForm
from accounts.models import CustomUser
from notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

@csrf_exempt
def assign_member(request, project_id, user_id):
    if request.method == "POST":
        try:
            project = Project.objects.get(id=project_id)
            member = User.objects.get(id=user_id)

            # Many-to-Many assignment
            project.assigned_to.add(member)
            project.save()

            return JsonResponse({"success": True, "message": "Assigned Successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)

# ✅ List all projects
@login_required
def project_list(request):

    # HR + Manager → SEE ALL PROJECTS (READ ONLY)
    if request.user.role in ["HR", "Manager"]:
        projects = Project.objects.all()
        return render(request, "projects/project_list_readonly.html", {
            "projects": projects,
            "readonly": True
        })

    # Team Member → see created or assigned projects
    projects = Project.objects.filter(
        owner=request.user
    ) | Project.objects.filter(
        assigned_to=request.user
    )

    return render(request, "projects/project_list.html", {
        "projects": projects.distinct(),
        "readonly": False
    })



# ✅ View single project detail + handle image uploads
@login_required
def project_detail(request, pk):
    """
    Managers and Team Members can both:
      ✅ View project details
      ✅ Upload images
      ✅ Add/update live project link
    """
    user = request.user

    if getattr(user, "role", None) == "Manager":
        project = get_object_or_404(Project, pk=pk)
    else:
        project = get_object_or_404(Project, Q(pk=pk) & (Q(owner=user) | Q(assigned_to=user)))

    images = project.images.all()
    form = ProjectImageForm()

    # ✅ Handle multiple image uploads
    if request.method == "POST":
        if "image" in request.FILES:
            files = request.FILES.getlist('image')
            for file in files:
                ProjectImage.objects.create(project=project, image=file, uploaded_by=user)
            messages.success(request, f"{len(files)} image(s) uploaded successfully!")
            return redirect('projects:project_detail', pk=pk)

        elif "live_link" in request.POST:
            live_link = request.POST.get("live_link")
            if live_link:
                project.live_link = live_link
                project.save(update_fields=["live_link"])
                messages.success(request, "🌐 Live project link updated successfully!")
            return redirect('projects:project_detail', pk=pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'images': images,
        'form': form,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user

            if getattr(request.user, "role", "") != "Manager":
                project.assigned_to = request.user

            project.save()
            messages.success(request, "🎉 Project created successfully!")
            return redirect('projects:project_list')
        else:
            # 🔍 Debug line: print form errors in console
            print("❌ FORM ERRORS:", form.errors)
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Create Project',
        'user': request.user,  # ensure template has user
    })


# ✅ Edit project
@login_required
def project_edit(request, pk):
    """Only project owner or manager can edit"""
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner and getattr(request.user, "role", None) != "Manager":
        messages.error(request, "❌ You are not authorized to edit this project.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Project updated successfully!")
            return redirect('projects:project_list')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ProjectForm(instance=project, user=request.user)

    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Edit Project'})


# ✅ Delete project
@login_required
def project_delete(request, pk):
    """Only project owner or manager can delete"""
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner and getattr(request.user, "role", None) != "Manager":
        messages.error(request, "❌ You are not authorized to delete this project.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        project.delete()
        messages.success(request, "🗑️ Project deleted successfully!")
        return redirect('projects:project_list')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})


# ✅ AJAX: Update project status
@login_required
@csrf_exempt
def update_status_ajax(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        new_status = request.POST.get("status")

        if new_status in ["Pending", "In Progress", "Completed", "On Hold"]:
            project.status = new_status
            project.save(update_fields=["status"])
            return JsonResponse({"success": True, "status": new_status})

        return JsonResponse({"success": False, "error": "Invalid status"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# ✅ AJAX: Update completion percentage
@login_required
@csrf_exempt
def update_completion_ajax(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        try:
            new_completion = int(request.POST.get("completion", 0))
            if 0 <= new_completion <= 100:
                project.completion = new_completion
                project.save(update_fields=["completion"])
                return JsonResponse({"success": True, "completion": new_completion})
            else:
                return JsonResponse({"success": False, "error": "Completion must be between 0–100"})
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid number"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# ✅ AJAX: Assign project to a team member (Manager only)
@login_required
@csrf_exempt
def assign_project_ajax(request, project_id):

    if request.method == "POST" and request.user.role == "Manager":
        project = get_object_or_404(Project, id=project_id)
        user_id = request.POST.get("assigned_to")

        if user_id:
            assigned_user = get_object_or_404(CustomUser, id=user_id)
            project.assigned_to = assigned_user
            project.save(update_fields=["assigned_to"])

            # 1️⃣ Create Notification DB Entry
            Notification.objects.create(
                user=assigned_user,
                message=f"You have been assigned to project: {project.name}",
                project=project
            )

            # 2️⃣ Send Real-Time WS Event
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                f"user_{assigned_user.id}",
                {
                    "type": "send_notification",
                    "data": {
                        "message": f"Assigned to project: {project.name}",
                        "project": project.id
                    }
                }
            )

            return JsonResponse({"success": True})

        return JsonResponse({"success": False})

# ✅ Delete uploaded image (Manager only)
@login_required
def delete_project_image(request, image_id):
    image = get_object_or_404(ProjectImage, id=image_id)
    project = image.project

    if getattr(request.user, "role", "") == "Manager":
        image.delete()
        messages.success(request, "🗑️ Image deleted successfully!")
    else:
        messages.error(request, "❌ You are not authorized to delete images.")

    return redirect('projects:project_detail', pk=project.id)

@login_required
def project_detail_readonly(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # HR and Manager: Read-only mode
    if request.user.role in ["HR", "Manager"]:
        tasks = Task.objects.filter(project=project)
        return render(request, "projects/project_detail_readonly.html", {
            "project": project,
            "tasks": tasks,
        })

    # Team Member → use old editable detail page
    return redirect("projects:project_detail", pk=pk)

