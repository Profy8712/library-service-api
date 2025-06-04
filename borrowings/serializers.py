from rest_framework import serializers
from books.serializers import BookSerializer
from users.serializers import UserSerializer

from borrowings.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]

class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["book", "expected_return_date"]

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError("This book is not available.")
        return value