from django.urls import path 
from users.views import SignUpView, LogInView


urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/login", LogInView.as_view()),
]