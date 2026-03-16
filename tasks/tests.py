from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Task, Category


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user,
            name="Study"
        )

    def test_task_string_representation(self):
        task = Task.objects.create(
            user=self.user,
            category=self.category,
            title="Finish coursework",
            description="Write implementation report",
            due_date=date.today(),
            completed=False
        )
        self.assertEqual(str(task), "Finish coursework")


class DashboardAccessTest(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, [302, 301])


class ToggleTaskStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="toggleuser",
            password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user,
            name="Personal"
        )
        self.task = Task.objects.create(
            user=self.user,
            category=self.category,
            title="Test toggle",
            description="Check complete status",
            due_date=date.today(),
            completed=False
        )

    def test_toggle_task_status(self):
        self.client.login(username="toggleuser", password="testpass123")

        response = self.client.get(reverse("toggle_task_status", args=[self.task.id]))
        self.assertIn(response.status_code, [200, 302])

        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)


class AnalyticsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="analyticsuser",
            password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user,
            name="Work"
        )
        Task.objects.create(
            user=self.user,
            category=self.category,
            title="Task 1",
            description="Completed task",
            due_date=date.today(),
            completed=True
        )
        Task.objects.create(
            user=self.user,
            category=self.category,
            title="Task 2",
            description="Pending task",
            due_date=date.today(),
            completed=False
        )

    def test_analytics_page_loads_for_logged_in_user(self):
        self.client.login(username="analyticsuser", password="testpass123")
        response = self.client.get(reverse("analytics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Analytics")