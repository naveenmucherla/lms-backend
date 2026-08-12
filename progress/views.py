from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import LessonProgress, CourseAssignment
from .serializers import CourseAssignmentSerializer
from courses.models import Lesson, Course
from accounts.models import User
from accounts.permissions import IsAdminOrMentor


class CompletedLessonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        completed = LessonProgress.objects.filter(
            student=request.user,
            lesson__chapter__course_id=course_id,
            completed=True
        ).values_list("lesson_id", flat=True)

        return Response(list(completed))


class LessonCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson
        )

        progress.completed = True
        progress.save()

        return Response({"message": "Lesson marked as completed"})


class AssignCourseView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrMentor]

    def get(self, request):
        assignments = CourseAssignment.objects.all().select_related('student', 'course')
        serializer = CourseAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    def post(self, request):
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")

        if not student_id or not course_id:
            return Response({"detail": "student_id and course_id are required"}, status=400)

        student = get_object_or_404(User, id=student_id, role="STUDENT")
        course = get_object_or_404(Course, id=course_id)

        assignment, created = CourseAssignment.objects.get_or_create(
            student=student,
            course=course
        )

        if not created:
            return Response({"detail": "Course already assigned to student"}, status=400)

        return Response({"message": "Course assigned successfully"}, status=201)

    def delete(self, request):
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")

        if not student_id or not course_id:
            return Response({"detail": "student_id and course_id are required"}, status=400)

        assignment = get_object_or_404(CourseAssignment, student_id=student_id, course_id=course_id)
        assignment.delete()

        return Response({"message": "Course unassigned successfully"})


class StudentEnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        assignment, created = CourseAssignment.objects.get_or_create(
            student=request.user,
            course=course
        )
        if not created:
            return Response({"detail": "You are already enrolled in this course"}, status=400)
        return Response({"message": f"Enrolled in {course.title} successfully!"}, status=201)
