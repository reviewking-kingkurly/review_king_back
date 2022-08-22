from django.urls import path, include

urlpatterns = [
    path('reviews', include('reviews.urls')),
    path("users", include("users.urls")),
    path("products", include("products.urls")),
]
