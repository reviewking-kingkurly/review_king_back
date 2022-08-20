from django.urls import path, include

urlpatterns = [
    path('reviews', include('reviews.urls')),
]
