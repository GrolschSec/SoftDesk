# Generated by Django 4.2.1 on 2023-06-06 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contributor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permissions",
                    models.CharField(
                        choices=[("LEAD", "Lead developer"), ("DEV", "Developer")],
                        max_length=4,
                    ),
                ),
                ("role", models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=2000)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("BE", "Back-end"),
                            ("FE", "Front-end"),
                            ("IOS", "iOS"),
                            ("AND", "Android"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "author_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authored_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        related_name="contributed_projects",
                        through="issues_tracking.Contributor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "tag",
                    models.CharField(
                        choices=[
                            ("BUG", "Bug"),
                            ("IMP", "Improvement"),
                            ("TSK", "Task"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("LOW", "Low"), ("MED", "Medium"), ("HIGH", "High")],
                        max_length=4,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("TODO", "To Do"),
                            ("ONGOING", "Ongoing"),
                            ("DONE", "Done"),
                        ],
                        max_length=7,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "assignee_user_id",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_issues",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "author_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authored_issues",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issues",
                        to="issues_tracking.project",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="issues_tracking.project",
            ),
        ),
        migrations.AddField(
            model_name="contributor",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authored_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="issues_tracking.issue",
                    ),
                ),
            ],
        ),
    ]
