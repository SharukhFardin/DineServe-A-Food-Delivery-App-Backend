from django.urls import path

from account.rest.views.me import UserLoginView, PublicUserRegistrationView

urlpatterns = [
    path("login", UserLoginView.as_view(), name="login"),
    path(
        "registration",
        PublicUserRegistrationView.as_view(),
        name="user.onboarding",
    ),
]
