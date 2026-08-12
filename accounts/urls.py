from django.urls import path
from .views import (
    StudentRegisterView,
    LoginView,
    StudentListView,
    AdminDeleteUserView,
    AdminCreateMentorView,
    MentorListView,
    AdminUsersView,
    UserProfileView,
)

urlpatterns = [
    path("register/", StudentRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserProfileView.as_view(), name="user-profile"),

    # Student / Mentor
    path("students/", StudentListView.as_view(), name="students"),
    path("mentors/", MentorListView.as_view(), name="mentors"),

    # Admin
    path("admin/users/", AdminUsersView.as_view(), name="admin-users"),
    path("admin/users/<int:user_id>/delete/", AdminDeleteUserView.as_view()),
    path("admin/create-mentor/", AdminCreateMentorView.as_view()),
]

