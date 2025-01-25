from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from users.models import Notification

from .forms import GiftForm, GiftSearchForm, ReviewForm, SavedSearchForm
from .models import Gift, Review, ReviewImage, ReviewVote, SavedSearch


class ListGifts(ListView):
    model = Gift
    template_name = "gifts/gifts.html"


def calculate_age(birth_date):
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def get_age_range(age):
    if age <= 12:
        return "0-12"
    if 13 <= age <= 17:
        return "13-17"
    if 18 <= age <= 24:
        return "18-24"
    if 25 <= age <= 34:
        return "25-34"
    if 35 <= age <= 50:
        return "35-50"
    return "50+"


class GiftCreateView(LoginRequiredMixin, CreateView):
    model = Gift
    form_class = GiftForm
    template_name = "gifts/create.html"
    success_url = reverse_lazy("users:wishlist")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Create Gift"
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.instance.suggestedBy = user

        response = super().form_valid(form)
        form.instance.hobbies.set(self.request.user.hobbies.all())

        if user.birth_date:
            age = calculate_age(user.birth_date)
            age_range = get_age_range(age)
            form.instance.suitable_age_range = age_range

        if user.gender:
            form.instance.suitable_gender = user.gender

        if user.location:
            form.instance.suitable_location = user.location

        form.instance.save()
        return response


class GiftUpdateView(LoginRequiredMixin, UpdateView):
    model = Gift
    form_class = GiftForm
    template_name = "gifts/edit.html"
    success_url = reverse_lazy("users:wishlist")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Update Gift"
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.suggestedBy != request.user:
            raise PermissionDenied("You are not allowed to edit this gift.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Gift updated!")
        return super().form_valid(form)


class SearchGiftView(ListView):
    model = Gift
    template_name = "gifts/search.html"
    context_object_name = "gifts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = GiftSearchForm(self.request.GET or None)

        if form.is_valid():
            category = form.cleaned_data.get("category")
            price_min = form.cleaned_data.get("price_min")
            price_max = form.cleaned_data.get("price_max")
            age = form.cleaned_data.get("age")
            gender = form.cleaned_data.get("gender")
            location = form.cleaned_data.get("location")
            order_by = form.cleaned_data.get("order_by", "-average_rating")

            if category:
                queryset = queryset.filter(giftCategories=category)
            if price_min is not None:
                queryset = queryset.filter(priceMin__gte=price_min)
            if price_max is not None:
                queryset = queryset.filter(priceMax__lte=price_max)
            if "hobbies" in self.request.GET and self.request.GET.getlist("hobbies"):
                queryset = queryset.filter(
                    hobbies__in=self.request.GET.getlist("hobbies")
                ).distinct()
            if age is not None:
                age_ranges = []
                if age <= 12:
                    age_ranges.append("0-12")
                elif 13 <= age <= 17:
                    age_ranges.append("13-17")
                elif 18 <= age <= 24:
                    age_ranges.append("18-24")
                elif 25 <= age <= 34:
                    age_ranges.append("25-34")
                elif 35 <= age <= 50:
                    age_ranges.append("35-50")
                else:
                    age_ranges.append("50+")
                queryset = queryset.filter(suitable_age_range__in=age_ranges)
            if gender:
                queryset = queryset.filter(suitable_gender__in=[gender, "U"])
            if location:
                queryset = queryset.filter(suitable_location__icontains=location)

            queryset = queryset.order_by(order_by or "-average_rating")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GiftSearchForm(self.request.GET or None)

        if self.request.GET.get("save_search") == "on":
            context["save_search_form"] = SavedSearchForm(
                initial={
                    "name": self.request.GET.get("search_name", "My Search"),
                    "category": self.request.GET.get("category"),
                    "price_min": self.request.GET.get("price_min"),
                    "price_max": self.request.GET.get("price_max"),
                    "age": self.request.GET.get("age"),
                    "gender": self.request.GET.get("gender"),
                    "location": self.request.GET.get("location"),
                    "order_by": self.request.GET.get("order_by", "-average_rating"),
                    "hobbies": self.request.GET.getlist("hobbies"),
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.user = request.user
            saved_search.save()
            form.save_m2m()
            messages.success(request, "Search saved successfully!")
            return redirect("gifts:saved_searches")
        else:
            messages.error(request, "There was an error saving your search.")
            return redirect("gifts:search")


@login_required
def mark_as_owned(request, pk):
    gift = get_object_or_404(Gift, pk=pk)
    user = request.user
    if gift not in user.possessed_gifts.all():
        user.possessed_gifts.add(gift)
        messages.success(request, "Gift marked as owned.")
    else:
        messages.info(request, "You already own this gift.")
    return redirect(request.META.get("HTTP_REFERER", "gifts:search"))


class GiftDetailView(DetailView):
    model = Gift
    template_name = "gifts/detail.html"
    context_object_name = "gift"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gift = self.get_object()
        context["reviews"] = gift.reviews.order_by("-created_at")
        context["average_rating"] = gift.average_rating
        context["review_form"] = ReviewForm()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        gift = self.get_object()

        if gift.suggestedBy == request.user:
            review_content_type = ContentType.objects.get_for_model(Review)
            reviews_in_gift = gift.reviews.values_list("id", flat=True)
            review_notifications_to_toggle = Notification.objects.filter(
                user=request.user,
                notification_type="new_review",
                content_type=review_content_type,
                object_id__in=reviews_in_gift,
                is_read=False,
            )
            review_notifications_to_toggle.update(is_read=True)

        gift_content_type = ContentType.objects.get_for_model(Gift)
        new_gift_notifications_to_toggle = Notification.objects.filter(
            user=request.user,
            notification_type="new_gift",
            content_type=gift_content_type,
            object_id=gift.id,
            is_read=False,
        )
        new_gift_notifications_to_toggle.update(is_read=True)

        return response


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "gifts/review_form.html"

    def form_valid(self, form):
        gift_id = self.kwargs["pk"]
        gift = get_object_or_404(Gift, id=gift_id)

        review = form.save(commit=False)
        review.gift = gift
        review.author = self.request.user
        review.save()

        files = self.request.FILES.getlist("images")
        for f in files:
            ReviewImage.objects.create(review=review, image=f)

        messages.success(self.request, "Review added successfully!")
        return redirect("gifts:detail", pk=gift_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gift_id = self.kwargs["pk"]
        gift = get_object_or_404(Gift, id=gift_id)
        context["gift"] = gift
        return context


@login_required
def upvote_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    try:
        vote_obj, created = ReviewVote.objects.get_or_create(
            review=review, user=request.user, defaults={"vote": 1}
        )
        if not created:
            # already voted
            if vote_obj.vote == 1:
                vote_obj.delete()
                messages.info(request, "Removed your upvote.")
            else:
                vote_obj.vote = 1
                vote_obj.save()
                messages.success(request, "You changed your vote to upvote.")
        else:
            messages.success(request, "Review upvoted!")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect(request.META.get("HTTP_REFERER", "gifts:list"))


@login_required
def downvote_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    try:
        vote_obj, created = ReviewVote.objects.get_or_create(
            review=review, user=request.user, defaults={"vote": -1}
        )
        if not created:
            if vote_obj.vote == -1:
                vote_obj.delete()
                messages.info(request, "Removed your downvote.")
            else:
                vote_obj.vote = -1
                vote_obj.save()
                messages.success(request, "You changed your vote to downvote.")
        else:
            messages.success(request, "Review downvoted!")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect(request.META.get("HTTP_REFERER", "gifts:list"))


class SaveSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        initial_data = {}
        search_fields = [
            "category",
            "price_min",
            "price_max",
            "age",
            "gender",
            "location",
            "hobbies",
            "order_by",
        ]
        for field in search_fields:
            if field == "hobbies":
                value = request.GET.getlist(field)
                if value:
                    initial_data[field] = value
            else:
                value = request.GET.get(field)
                if value:
                    initial_data[field] = value
        form = SavedSearchForm(initial=initial_data)
        return render(request, "gifts/save_search.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.user = request.user
            saved_search.save()
            form.save_m2m()
            messages.success(request, "Search saved successfully!")
            return redirect("gifts:saved_searches")
        else:
            messages.error(request, "There was an error saving your search.")
            return render(request, "gifts/save_search.html", {"form": form})


class SavedSearchListView(LoginRequiredMixin, ListView):
    model = SavedSearch
    template_name = "gifts/saved_searches.html"
    context_object_name = "saved_searches"

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class SavedSearchDeleteView(LoginRequiredMixin, DeleteView):
    model = SavedSearch
    template_name = "gifts/delete_saved_search.html"
    success_url = reverse_lazy("gifts:saved_searches")

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Saved search deleted successfully!")
        return super().delete(request, *args, **kwargs)


@login_required
def execute_saved_search(request, pk):
    saved_search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    query_params = {
        "category": saved_search.category.id if saved_search.category else "",
        "price_min": saved_search.price_min or "",
        "price_max": saved_search.price_max or "",
        "age": saved_search.age or "",
        "gender": saved_search.gender or "",
        "location": saved_search.location or "",
        "order_by": saved_search.order_by or "-average_rating",
    }

    hobbies = saved_search.hobbies.all()
    if hobbies.exists():
        query_params["hobbies"] = [h.id for h in hobbies]

    from urllib.parse import urlencode

    encoded_params = urlencode(query_params, doseq=True)
    return redirect(f"{reverse_lazy('gifts:search')}?{encoded_params}")
