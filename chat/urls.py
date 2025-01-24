from django.urls import path

from .views import chat_room

app_name = "chat"

urlpatterns = [
    path("chat_with/<int:pk>/", chat_room, name="chat_room"),
]
