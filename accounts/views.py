from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsMentor, IsAdmin
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

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
    

User = get_user_model()

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


class InitDBView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            from django.core.management import call_command
            from seed_data import seed_database
            call_command("migrate", interactive=False)
            seed_database()
            return Response({"status": "Database migrated and seeded successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)