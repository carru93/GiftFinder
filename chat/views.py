from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from users.models import Notification, User

from .models import Message
from .utils import get_room_name_for_users


@login_required
def chat_room(request, pk):
    destination_user = get_object_or_404(User, pk=pk)

    if destination_user == request.user:
        return HttpResponseForbidden("Cannot chat with yourself.")

    room_name = get_room_name_for_users(request.user.id, destination_user.id)

    messages_qs = Message.objects.filter(
        sender__in=[request.user, destination_user],
        receiver__in=[request.user, destination_user],
    ).order_by("timestamp")

    message_content_type = ContentType.objects.get_for_model(Message)
    messages_in_room = Message.objects.filter(room_name=room_name).values_list(
        "id", flat=True
    )
    notifications_to_mark = Notification.objects.filter(
        user=request.user,
        notification_type="new_message",
        content_type=message_content_type,
        object_id__in=messages_in_room,
        is_read=False,
    )

    notifications_to_mark.update(is_read=True)

    return render(
        request,
        "chat/chat_room.html",
        {
            "room_name": room_name,
            "destination_user": destination_user,
            "chat_messages": messages_qs,
        },
    )
