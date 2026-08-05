from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from accounts.models import User
from .models import Notification


def create_notification(user, message):

    notification = Notification.objects.create(
        recipient=user,
        message=message
    )

    unread_count = Notification.objects.filter(
        recipient=user,
        is_read=False
    ).count()


    channel_layer = get_channel_layer()

    notification_count = Notification.objects.filter(
    recipient=user,
    is_read=False
    ).count()


    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": message,
            "count": notification_count,
        },
    )

    print("Notification sent to channel")


def notify_receptionists(message):

    receptionists = User.objects.filter(
        role="receptionist"
    )

    for receptionist in receptionists:
        print(f"Sending to {receptionist.username}")

        create_notification(
            receptionist,
            message
        )
def notify_doctors(message):

    doctors = User.objects.filter(
        role="doctor"
    )

    for doctor in doctors:

        create_notification(
            doctor,
            message
        )
def notify_patient(patient, message):

    if patient.user:

        create_notification(
            patient.user,
            message
        )