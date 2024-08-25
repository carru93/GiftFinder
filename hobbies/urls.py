from django.urls import path

from .autocomplete import HobbyAutocomplete

app_name = "hobbies"

urlpatterns = [
    path("autocomplete/", HobbyAutocomplete.as_view(), name="autocomplete"),
]
