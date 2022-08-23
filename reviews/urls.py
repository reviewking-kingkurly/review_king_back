from django.urls import path

from reviews.views import ReviewView, WriteReviewView, ReviewDetailView, WriteReviewListView, BestReviewListView, ReviewRankingCategoryView, ReviewLikeView, ReviewListView

urlpatterns = [
    path('', ReviewView.as_view()),
    path('/write/<int:ordered_item_id>', WriteReviewView.as_view()),
    path('/<int:review_id>', ReviewDetailView.as_view()),
    path('/write_list', WriteReviewListView.as_view()),
    path('/best', BestReviewListView.as_view()),
    path('/ranking', ReviewRankingCategoryView.as_view()),
    path('/like', ReviewLikeView.as_view()),
    path('/list/<int:product_id>', ReviewListView.as_view()),
]