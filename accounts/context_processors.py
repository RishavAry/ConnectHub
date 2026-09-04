from .models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        unread_count = request.user.received_notifications.filter(
            is_read=False
        ).count()
    else:
        unread_count = 0

    return {
        "unread_count": unread_count
    }