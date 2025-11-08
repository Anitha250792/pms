from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import chain

from .models import Project, ProjectImage
from .forms import ProjectForm, ProjectImageForm
from accounts.models import CustomUser


# ✅ List all projects
@login_required
def project_list(request):
    """
    Manager → See all projects
    Team Member → See both owned and assigned projects
    """
    user = request.user

    if getattr(user, "role", None) == "Manager":
        # Manager sees all projects
        projects = Project.objects.all().order_by('-id')
    else:
        # Team member sees both owned and assigned projects
        owned_projects = Project.objects.filter(owner=user)
        assigned_projects = Project.objects.filter(assigned_to=user)
        projects = list(chain(owned_projects, assigned_projects))  # merge

    return render(request, 'projects/project_list.html', {'projects': projects})


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

    # Access restriction: team members see only their projects
    if getattr(user, "role", None) == "Manager":
        project = get_object_or_404(Project, pk=pk)
    else:
        project = get_object_or_404(Project, Q(pk=pk) & (Q(owner=user) | Q(assigned_to=user)))

    images = project.images.all()
    form = ProjectImageForm()

    # ✅ Handle multiple image uploads
    if request.method == "POST":
        # If images are uploaded
        if "image" in request.FILES:
            files = request.FILES.getlist('image')
            for file in files:
                ProjectImage.objects.create(project=project, image=file, uploaded_by=user)
            messages.success(request, f"{len(files)} image(s) uploaded successfully!")
            return redirect('projects:project_detail', pk=pk)

        # ✅ Handle live link update
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



# ✅ Create new project
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user

            # Auto-assign team member if non-manager creates it
            if getattr(request.user, "role", "") != "Manager":
                project.assigned_to = request.user

            project.save()
            messages.success(request, "🎉 Project created successfully!")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create Project'})


# ✅ Edit project
@login_required
def project_edit(request, pk):
    """Only project owner or manager can edit"""
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner and getattr(request.user, "role", None) != "Manager":
        messages.error(request, "❌ You are not authorized to edit this project.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Project updated successfully!")
            return redirect('projects:project_list')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ProjectForm(instance=project)

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
    if request.method == "POST" and getattr(request.user, "role", "") == "Manager":
        project = get_object_or_404(Project, id=project_id)
        user_id = request.POST.get("assigned_to")

        if user_id:
            assigned_user = get_object_or_404(CustomUser, id=user_id)
            project.assigned_to = assigned_user
            project.save(update_fields=["assigned_to"])
            return JsonResponse({
                "success": True,
                "assigned_to": assigned_user.username
            })

        return JsonResponse({"success": False, "error": "No user selected"})

    return JsonResponse({"success": False, "error": "Invalid request"})


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
