from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

User = get_user_model()


class BookPermissionsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=5,
            daily_fee=1.99,
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            password="userpass",
        )

    def test_unauthenticated_access(self) -> None:
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse("book-list"),
            data={
                "title": "New Book",
                "author": "New Author",
                "cover": "SOFT",
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_access(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse("book-list"),
            data={
                "title": "New Book",
                "author": "New Author",
                "cover": "SOFT",
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_admin_access(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("book-list"),
            data={
                "title": "New Book",
                "author": "New Author",
                "cover": "SOFT",
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
