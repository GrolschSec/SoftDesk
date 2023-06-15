from rest_framework.permissions import BasePermission
from .models import Contributor, Project
from django.core.exceptions import ObjectDoesNotExist


class IsProjectAuthor(BasePermission):
    """
    Check if the user is the author of the project to update, destroy
    and if the user is either author or contributor to retrieve the project.
    """

    def has_object_permission(self, request, view, obj):
        if view.action in ("update", "destroy"):
            return obj.author_user_id == request.user
        elif view.action == "retrieve":
            return (
                obj.contributors.filter(id=request.user.id).exists()
                or obj.author_user_id == request.user
            )
        return True


class IsAuthorContributor(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Project.objects.get(id=view.kwargs["project_id"])
        except ObjectDoesNotExist:
            return False
        if view.action in ("create", "update", "destroy"):
            return project.author_user_id == request.user
        elif view.action == "list":
            return (
                request.user == project.author_user_id
                or project.contributors.filter(id=request.user.id).exists()
            )


class IsContributorIssue(BasePermission):
    def has_permission(self, request, view):
        if view.action == "retrieve":
            return False
        elif view.action in ("create", "list"):
            try:
                project = Project.objects.get(id=view.kwargs["project_id"])
            except ObjectDoesNotExist:
                return False
            return (
                request.user == project.author_user_id
                or project.contributors.filter(id=request.user.id).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ("update", "delete"):
            return request.user == obj.author_user_id
        return False


class IsContributorComment(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Project.objects.get(id=view.kwargs["project_id"])
        except ObjectDoesNotExist:
            return False
        if view.action in ("create", "list", "retrieve"):
            return (
                request.user == project.author_user_id
                or project.contributors.filter(id=request.user.id).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ("update", "delete"):
            return request.user == obj.author_user_id
        return False
