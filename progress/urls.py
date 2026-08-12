from django.urls import path
from .views import CompletedLessonsView, LessonCompleteView, AssignCourseView, StudentEnrollView

urlpatterns = [
    path(
        "course/<int:course_id>/completed-lessons/",
        CompletedLessonsView.as_view()
    ),
    path(
        "lesson/<int:lesson_id>/complete/",
        LessonCompleteView.as_view()
    ),
    path(
        "assign/",
        AssignCourseView.as_view()
    ),
    path(
        "enroll/<int:course_id>/",
        StudentEnrollView.as_view()
    ),
]


