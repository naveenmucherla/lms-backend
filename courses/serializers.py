from rest_framework import serializers
from .models import Course, Chapter, Lesson
from accounts.models import User



class CourseSerializer(serializers.ModelSerializer):
    mentor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="MENTOR")
    )
    mentor_name = serializers.CharField(
        source="mentor.username", read_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "mentor",
            "mentor_name",
            "created_at",
        ]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
        ]



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "video_url",
            "order",
            "chapter"
        ]
        extra_kwargs = {
            "chapter": {"required": False}
        }


