from django.urls import path
from .views import LessonCreateView, LessonListView, LessonDeleteView
from .views import AdminCourseListCreateView, AdminCourseCreateView, AdminCourseDeleteView

from .views import (
    CourseCreateView,
    CourseListView,
    ChapterCreateView,
    MyCoursesView,
    AdminChapterDeleteView,
    AdminChapterListCreateView,
    AdminChapterCreateView,
    StudentCourseProgressView,
    LessonCompleteView,
    ChapterListView,
    StudentChapterListView,
    CourseStudentsProgressView,
)

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("create/", CourseCreateView.as_view(), name="course-create"),
    path("my-courses/", MyCoursesView.as_view(), name="my-courses"),
    path("<int:course_id>/chapters/create/", ChapterCreateView.as_view(), name="chapter-create"),
    path("admin/", AdminCourseListCreateView.as_view()),
    path("admin/<int:pk>/delete/", AdminCourseDeleteView.as_view()),
    path("admin/<int:course_id>/chapters/create/", ChapterCreateView.as_view()),
    path("admin/create/", AdminCourseCreateView.as_view()),
    path("admin/<int:course_id>/chapters/", AdminChapterListCreateView.as_view()),
    path("admin/chapters/<int:pk>/delete/", AdminChapterDeleteView.as_view()),
    path("admin/<int:course_id>/chapters/", AdminChapterCreateView.as_view(), name="admin-create-chapter"),
    path("student/<int:course_id>/progress/", StudentCourseProgressView.as_view(), name="student-course-progress"),
    path("lessons/<int:lesson_id>/complete/", LessonCompleteView.as_view()),
    path("lessons/<int:pk>/delete/", LessonDeleteView.as_view(), name="lesson-delete"),
    path("courses/<int:course_id>/chapters/", ChapterListView.as_view(), name="course-chapters"),
    path("lessons/chapter/<int:chapter_id>/", LessonListView.as_view(), name="chapter-lessons"),
    path("student/<int:course_id>/chapters/", StudentChapterListView.as_view(), name="student-course-chapters"),
    path("lessons/chapter/<int:chapter_id>/create/", LessonCreateView.as_view(), name="lesson-create"),
    path("admin/course/<int:course_id>/students-progress/", CourseStudentsProgressView.as_view(), name="course-students-progress"),
]

urlpatterns += [
    path(
        "chapters/<int:chapter_id>/lessons/",
        LessonListView.as_view(),
        name="lesson-list"
    ),
    path(
        "chapters/<int:chapter_id>/lessons/create/",
        LessonCreateView.as_view(),
        name="lesson-create"
    ),
]