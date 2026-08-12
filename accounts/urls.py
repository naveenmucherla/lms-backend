from django.urls import path
from .views import (
    StudentRegisterView,
    LoginView,
    StudentListView,
    AdminDeleteUserView,
    AdminCreateMentorView,
    MentorListView,
    AdminUsersView,
    InitDBView,
)

urlpatterns = [
    path("init-db/", InitDBView.as_view(), name="init-db"),
    path("register/", StudentRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Student / Mentor
    path("students/", StudentListView.as_view(), name="students"),
    path("mentors/", MentorListView.as_view(), name="mentors"),

    # Admin
    path("admin/users/", AdminUsersView.as_view(), name="admin-users"),
    path("admin/users/<int:user_id>/delete/", AdminDeleteUserView.as_view()),
    path("admin/create-mentor/", AdminCreateMentorView.as_view()),
]
