from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False
        ).order_by("-timestamp")[:10]
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    return {"notifications": unread_notifications, "unread_count": unread_count}
