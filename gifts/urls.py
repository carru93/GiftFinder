from django.urls import path
from .views import ListGifts, GiftCreateView

app_name="gifts"

urlpatterns = [
    path('', ListGifts.as_view(), name='list'),
    path('new/', GiftCreateView.as_view(), name='create'),
]
