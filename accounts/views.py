from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsMentor, IsAdmin
from .serializers import RegisterSerializer, UserSerializer

class StudentRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["username"] = user.username

        return token




class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]




class StudentListView(APIView):
    permission_classes = [IsAuthenticated, IsMentor | IsAdmin]

    def get(self, request):
        students = User.objects.filter(role="STUDENT")
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)


class AdminUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AdminDeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        # Prevent admin deleting themselves
        if user == request.user:
            return Response(
                {"detail": "You cannot delete yourself"},
                status=400
            )

        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=200
        )


class AdminCreateMentorView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists"},
                status=400
            )

        mentor = User.objects.create_user(
            username=username,
            password=password,
            role="MENTOR",
            is_active=True
        )

        return Response(
            {
                "message": "Mentor created successfully",
                "mentor_id": mentor.id,
                "username": mentor.username
            },
            status=201
        )

class MentorListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role="MENTOR")
    
class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)