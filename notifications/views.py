from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

@login_required
def mark_notifications_read(request):

    print("==========")
    print("MARK READ CALLED")
    print(request.user.username)

    unread = request.user.notifications.filter(
        is_read=False
    )

    print("Unread before:", unread.count())

    unread.update(is_read=True)

    print(
        "Unread after:",
        request.user.notifications.filter(
            is_read=False
        ).count()
    )

    return JsonResponse({
        "success": True
    })