from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPES = (
        ("BE", "Back-end"),
        ("FE", "Front-end"),
        ("IOS", "iOS"),
        ("AND", "Android"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    type = models.CharField(max_length=3, choices=TYPES)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Contributor",
        related_name="contributed_projects",
    )
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )


class Contributor(models.Model):
    PERMISSIONS = (
        ("LEAD", "Lead developer"),
        ("DEV", "Developer")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=4, choices=PERMISSIONS)
    role = models.CharField(max_length=80, null=True, blank=True)


class Issue(models.Model):
    TAGS = (
        ("BUG", "Bug"),
        ("IMP", "Improvement"),
        ("TSK", "Task"),
    )
    PRIORITIES = (
        ("LOW", "Low"),
        ("MED", "Medium"),
        ("HIGH", "High"),
    )
    STATUSES = (
        ("TODO", "To Do"),
        ("ONGOING", "Ongoing"),
        ("DONE", "Done"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=3, choices=TAGS)
    priority = models.CharField(max_length=4, choices=PRIORITIES)
    status = models.CharField(max_length=7, choices=STATUSES)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )
    assignee_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
        default=None,
        blank=True,
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.assignee_user_id is None:
            self.assignee_user_id = self.author_user_id
        super().save(*args, **kwargs)


class Comment(models.Model):
    description = models.TextField()
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_comments",
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)
