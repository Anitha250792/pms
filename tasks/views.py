from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import Task
from .forms import TaskForm
from accounts.models import CustomUser


# -----------------------------------------------------
# 🧩 Task List View
# -----------------------------------------------------
@login_required
def task_list(request):

    # HR + Manager → VIEW ALL TASKS
    if request.user.role in ["HR", "Manager"]:
        tasks = Task.objects.all()
        return render(request, "tasks/task_list_readonly.html", {
            "tasks": tasks,
            "readonly": True
        })

    # Team Member → only assigned tasks
    tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "readonly": False
    })

# -----------------------------------------------------
# 🧩 Task Detail View
# -----------------------------------------------------
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Manager can only view if not assigned
    readonly = (request.user.role == "Manager" and task.assigned_to != request.user)

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "readonly": readonly
    })


# -----------------------------------------------------
# 🧩 Task Create View
# -----------------------------------------------------
@login_required
def task_create(request):
    """
    Only employees can create tasks.
    (If you want managers to create too, remove the role check.)
    """
    if request.user.role == "Manager":
        return HttpResponseForbidden("Managers cannot create tasks from this view.")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.owner = request.user  # ✅ ensure owner field exists in model
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect("tasks:task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})


# -----------------------------------------------------
# 🧩 AJAX — Update Task Status
# -----------------------------------------------------
@login_required
def update_task_status(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get("status")

        if new_status in ["Pending", "In Progress", "Completed"]:
            task.status = new_status
            task.save(update_fields=["status"])
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid status"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


# -----------------------------------------------------
# 🧩 AJAX — Update Task Completion Percentage
# -----------------------------------------------------
@login_required
def update_task_completion(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        try:
            completion = int(request.POST.get("completion", 0))
            if 0 <= completion <= 100:
                task.completion = completion
                if completion == 100:
                    task.status = "Completed"
                elif completion > 0 and task.status == "Pending":
                    task.status = "In Progress"
                task.save(update_fields=["completion", "status"])
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Completion must be between 0–100"})
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid completion value"})
    return JsonResponse({"success": False, "error": "Invalid request method"})

# -----------------------------------------------------
# 🧩 Task Edit View
# -----------------------------------------------------
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Only assigned user or owner can edit
    if request.user != task.assigned_to and request.user != task.owner:
        messages.error(request, "You are not authorized to edit this task.")
        return redirect("tasks:task_detail", pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # ✅ Saves completion, status, etc.
            messages.success(request, "Task updated successfully.")
            return redirect("tasks:task_list")  # ✅ redirect back to list to show update
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form, "task": task})



# -----------------------------------------------------
# 🧩 Task Delete View
# -----------------------------------------------------
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Only assigned user or owner can delete
    if request.user != task.assigned_to and request.user != getattr(task, 'owner', None):
        messages.error(request, "You are not authorized to delete this task.")
        return redirect("tasks:task_detail", pk=pk)

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("tasks:task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})

@login_required
def task_detail_readonly(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # HR and Manager view → Read Only
    if request.user.role in ["HR", "Manager"]:
        return render(request, "tasks/task_detail_readonly.html", {
            "task": task,
        })

    # Team Member → normal editable view
    return redirect("tasks:task_detail", pk=pk)

