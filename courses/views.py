from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsAdmin, IsMentor, IsStudent, IsAdminOrMentor
from progress.models import CourseAssignment, LessonProgress
# pyrefly: ignore [missing-import]
from .models import Course, Chapter, Lesson
from .serializers import CourseSerializer, ChapterSerializer, LessonSerializer

class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsMentor]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

class StudentChapterListView(ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Chapter.objects.filter(
            course_id=self.kwargs["course_id"]
        )

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()


class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        assignments = CourseAssignment.objects.filter(student=request.user)
        courses = [a.course for a in assignments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMentor]

    def perform_create(self, serializer):
        chapter = get_object_or_404(Chapter, id=self.kwargs["chapter_id"])
        serializer.save(chapter=chapter)



class LessonListView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(
            chapter_id=self.kwargs["chapter_id"]
        ).order_by("order")
    

class AdminCourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AdminCourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

class ChapterCreateView(generics.CreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMentor]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)


class AdminCourseCreateView(CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save()


class AdminChapterListCreateView(ListCreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        course_id = self.kwargs["course_id"]
        return Chapter.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)


class AdminChapterDeleteView(DestroyAPIView):
    queryset = Chapter.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

class AdminChapterCreateView(generics.CreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)


class StudentCourseProgressView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, course_id):
        # Total lessons in the course
        total_lessons = Lesson.objects.filter(
            chapter__course_id=course_id
        ).count()

        # Lessons completed by THIS student
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__chapter__course_id=course_id,
            completed=True
        ).count()

        percentage = 0
        if total_lessons > 0:
            percentage = int((completed_lessons / total_lessons) * 100)

        return Response({
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "percentage": percentage,
            "completed": percentage == 100
        })

def get_progress(student, course):
    total = Lesson.objects.filter(chapter__course=course).count()
    completed = LessonProgress.objects.filter(
        student=student,
        lesson__chapter__course=course
    ).count()
     
     
    return 0 if total == 0 else int((completed / total) * 100)


class LessonCompleteView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson
        )

        progress.completed = True
        progress.save()

        return Response({
            "message": "Lesson marked as completed"
        })

class ChapterListView(ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chapter.objects.filter(
            course_id=self.kwargs["course_id"]
        )




class CourseStudentsProgressView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrMentor]

    def get(self, request, course_id):
        # total lessons in course
        total_lessons = Lesson.objects.filter(
            chapter__course_id=course_id
        ).count()

        students = User.objects.filter(role="STUDENT")

        data = []
        for student in students:
            completed = LessonProgress.objects.filter(
                student=student,
                lesson__chapter__course_id=course_id,
                completed=True
            ).count()

            percentage = 0
            if total_lessons > 0:
                percentage = int((completed / total_lessons) * 100)

            data.append({
                "student_id": student.id,
                "student_name": student.username,
                "completed_lessons": completed,
                "total_lessons": total_lessons,
                "percentage": percentage
            })

        return Response(data)


class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrMentor]

