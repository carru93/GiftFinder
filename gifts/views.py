from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import GiftForm, GiftSearchForm, ReviewForm
from .models import Gift, Review, ReviewImage, ReviewVote


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
        queryset = queryset.order_by("-average_rating")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GiftSearchForm(self.request.GET or None)
        return context


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
