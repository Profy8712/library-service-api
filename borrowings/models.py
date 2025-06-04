from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(default=timezone.now)
    expected_return_date = models.DateField(
        validators=[MinValueValidator(limit_value=timezone.now().date())]
    )
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.book.title}"

    class Meta:
        ordering = ["-borrow_date"]

