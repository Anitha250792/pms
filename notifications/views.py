from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    """Show all notifications in a page"""
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/list.html", {"notifications": notifications})

@login_required
def get_unread_notifications(request):
    """API endpoint for unread badge count"""
    notes = Notification.objects.filter(user=request.user, is_read=False)

    return JsonResponse({
        "count": notes.count(),
        "items": [
            {
                "id": n.id,
                "message": n.message,
                "link": n.link or "#",
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for n in notes
        ]
    })

@login_required
def mark_as_read(request, note_id):
    Notification.objects.filter(id=note_id, user=request.user).update(is_read=True)
    return JsonResponse({"success": True})
