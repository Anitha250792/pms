from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Message
from .forms import MessageForm
from projects.models import Project
from tasks.models import Task
from accounts.models import CustomUser


# ==========================
# HR DASHBOARD
# ==========================
@login_required
def hr_dashboard(request):
    """
    HR can see everything in read-only mode:
    ✔ All projects
    ✔ All tasks
    ✔ All managers & team members
    ✔ HR message composer
    ✔ Recent messages
    """
    messages_list = Message.objects.all().order_by("-created_at")[:50]
    form = MessageForm()

    context = {
        "form": form,
        "messages": messages_list,
        "projects": Project.objects.all(),
        "tasks": Task.objects.all(),
        "team": CustomUser.objects.all(),
    }
    return render(request, "dashboard/hr_dashboard.html", context)


# ==========================
# HR POSTS ANNOUNCEMENT
# ==========================
@login_required
@require_POST
def post_announcement(request):

    if request.user.role != "HR":
        return HttpResponseForbidden("Only HR can post announcements.")

    form = MessageForm(request.POST)

    if form.is_valid():
        msg = form.save(commit=False)
        msg.sender = request.user
        msg.created_at = timezone.now()
        msg.save()

        # Send message via WebSocket broadcast
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "announcements",
            {
                "type": "announce.message",
                "id": msg.id,
                "sender": msg.sender.username,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "errors": form.errors})


# ==========================
# FETCH ANNOUNCEMENTS (AJAX)
# ==========================
@login_required
def get_announcements(request):

    msgs = Message.objects.all().order_by("-id")[:1]

    data = [
        {
            "id": m.id,
            "sender": m.sender.username if m.sender else "HR",
            "content": m.content,
            "created_at": m.created_at.isoformat(),
        }
        for m in msgs
    ]

    return JsonResponse({"messages": data})
