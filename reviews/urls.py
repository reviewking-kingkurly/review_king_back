from django.urls import path

from reviews.views import ReviewView

urlpatterns = [
    path('', ReviewView.as_view()),
]