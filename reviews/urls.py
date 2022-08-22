from django.urls import path

from reviews.views import ReviewView, ReviewDetailView, WriteReviewListView, BestReviewListView

urlpatterns = [
    path('', ReviewView.as_view()),
    path('/<int:review_id>', ReviewDetailView.as_view()),
    path('/write_list', WriteReviewListView.as_view()),
    path('/best', BestReviewListView.as_view()),
]