from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False, default='STUDENT')

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.get('role', 'STUDENT').upper()
        if role not in ['STUDENT', 'MENTOR', 'ADMIN']:
            role = 'STUDENT'
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role
        )
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]