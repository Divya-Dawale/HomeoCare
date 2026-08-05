from .models import Notification


def notifications(request):

    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by(
            "-created_at"
        )[:10]


        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()


        return {

            "notifications": notifications,
            "notification_count": unread_count,

        }


    return {

        "notifications": [],
        "notification_count": 0,

    }