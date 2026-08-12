from rest_framework import serializers
from .models import CourseAssignment


class CourseAssignmentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = CourseAssignment
        fields = ['id', 'student', 'course', 'assigned_at']
