"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from issues_tracking.views import (
    UserSignupViewset,
    UserLoginViewset,
    ProjectViewset,
    ContributorsViewset,
    IssuesViewset,
    CommentsViewset,
)
from django.contrib import admin


router = SimpleRouter()
router.register("signup", UserSignupViewset, basename="signup")
router.register("login", UserLoginViewset, basename="login")
router.register("projects", ProjectViewset, basename="projects")
router.register(
    r"projects/(?P<project_id>\d+)/users", ContributorsViewset, basename="project-users"
)
router.register(
    r"projects/(?P<project_id>\d+)/issues", IssuesViewset, basename="project-issues"
)
router.register(
    r"projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments",
    CommentsViewset,
    basename="issues-comments",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
