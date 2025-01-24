from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from users.models import User

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

    return render(
        request,
        "chat/chat_room.html",
        {
            "room_name": room_name,
            "destination_user": destination_user,
            "messages": messages_qs,
        },
    )
