from dal.autocomplete import Select2QuerySetView

from hobbies.models import Hobby


class HobbyAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Hobby.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
