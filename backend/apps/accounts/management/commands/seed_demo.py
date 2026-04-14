import logging

from django.core.management.base import BaseCommand
from django.db import transaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database with demo data for QAA training."

    @transaction.atomic
    def handle(self, *args, **options):
        from apps.accounts.models import User
        from apps.projects.models import Project, ProjectMember
        from apps.tasks.models import Task
        from apps.comments.models import Comment

        self.stdout.write("Seeding demo data...")

        # Clear existing demo data to make the command idempotent
        User.objects.filter(username__in=["admin", "alice", "bob", "charlie"]).delete()

        # Users
        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
            role="admin",
        )
        alice = User.objects.create_user(
            username="alice", password="pass123", email="alice@example.com"
        )
        bob = User.objects.create_user(
            username="bob", password="pass123", email="bob@example.com"
        )
        charlie = User.objects.create_user(
            username="charlie", password="pass123", email="charlie@example.com"
        )

        self.stdout.write(f"  Created users: {admin}, {alice}, {bob}, {charlie}")

        # Projects
        project1 = Project.objects.create(
            title="Alpha Project",
            description="First demo project for QAA training.",
            status="active",
            owner=alice,
        )
        project2 = Project.objects.create(
            title="Beta Project",
            description="Second demo project with archived status.",
            status="archived",
            owner=alice,
        )

        # Members
        ProjectMember.objects.create(project=project1, user=bob)

        self.stdout.write(f"  Created projects: {project1}, {project2}")
        self.stdout.write(f"  Bob added as member of {project1}")

        # Tasks for project1
        task1 = Task.objects.create(
            project=project1,
            title="Write unit tests",
            description="Cover all API endpoints with unit tests.",
            status="todo",
            priority="high",
            created_by=alice,
            assignee=bob,
        )
        task2 = Task.objects.create(
            project=project1,
            title="Set up CI pipeline",
            description="Configure GitHub Actions for automated testing.",
            status="in_progress",
            priority="medium",
            created_by=alice,
        )
        task3 = Task.objects.create(
            project=project1,
            title="Update documentation",
            description="Keep API docs in sync with implementation.",
            status="done",
            priority="low",
            created_by=bob,
        )

        # Tasks for project2
        task4 = Task.objects.create(
            project=project2,
            title="Design database schema",
            description="ER diagram and migration plan.",
            status="done",
            priority="high",
            created_by=alice,
        )
        task5 = Task.objects.create(
            project=project2,
            title="Implement search feature",
            description="Global search across projects and tasks.",
            status="todo",
            priority="medium",
            created_by=alice,
        )

        self.stdout.write(
            f"  Created tasks: {task1}, {task2}, {task3}, {task4}, {task5}"
        )

        # Comments on task1
        comment1 = Comment.objects.create(
            task=task1,
            author=alice,
            body="Tests should cover happy path and all error cases (400, 401, 403, 404).",
        )
        comment2 = Comment.objects.create(
            task=task1,
            author=bob,
            body="I'll start with the auth endpoints — they're the most critical.",
        )

        self.stdout.write(f"  Created comments: {comment1}, {comment2}")

        self.stdout.write(self.style.SUCCESS("\nSeed complete. Summary:"))
        self.stdout.write(f"  Users   : admin / admin123, alice / pass123, bob / pass123, charlie / pass123")
        self.stdout.write(f"  Projects: {project1.title} (active), {project2.title} (archived)")
        self.stdout.write(f"  Tasks   : {Task.objects.count()} total")
        self.stdout.write(f"  Comments: {Comment.objects.count()} total")
