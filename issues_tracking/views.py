from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)
from .models import Project, Contributor, Issue, Comment
from .permissions import (
    IsProjectAuthor,
    IsAuthorContributor,
    IsContributorIssue,
    IsContributorComment,
)
from django.db.models import Q


class UserSignupViewset(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        if self.queryset.filter(email=email).exists():
            raise ValidationError("A user with this email already exist.")
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh_token": str(refresh), "access_token": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserLoginViewset(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username/password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh_token": str(refresh), "access_token": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    authentication_classes = [JWTAuthentication]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            return Project.objects.filter(Q(author_user_id=user) | Q(contributors=user))
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)


class ContributorsViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorContributor]
    authentication_classes = [JWTAuthentication]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Contributor.objects.filter(project__id=self.kwargs.get("project_id"))

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs.get("project_id"))
        user_id = self.request.data.get("user")
        user = get_object_or_404(User, id=user_id)
        if project.contributors.filter(id=user_id).exists():
            raise ValidationError("This user is already a contributor to the project.")
        serializer.save(project=project, user=user)


class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorIssue]
    authentication_classes = [JWTAuthentication]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Issue.objects.filter(project__id=self.kwargs.get("project_id"))

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs.get("project_id"))
        serializer.save(author_user_id=self.request.user, project=project)


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorComment]
    authentication_classes = [JWTAuthentication]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs.get("issue_id"))

    def perform_create(self, serializer):
        get_object_or_404(Project, id=self.kwargs.get("project_id"))
        issue = get_object_or_404(Issue, id=self.kwargs.get("issue_id"))
        serializer.save(author_user_id=self.request.user, issue=issue)
