from django.urls import path

from .views import (
    ScholarApplicationView,
    ScholarProfileView,
    ScholarReviewListCreateView,
    ScholarReviewQueueView,
)

urlpatterns = [
    path('me/', ScholarProfileView.as_view(), name='scholar-profile'),
    path('applications/', ScholarApplicationView.as_view(), name='scholar-application'),
    path('reviews/', ScholarReviewListCreateView.as_view(), name='scholar-reviews'),
    path('review-queue/', ScholarReviewQueueView.as_view(), name='scholar-review-queue'),
]
