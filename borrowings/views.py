from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django_filters import rest_framework as filters

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingReadSerializer, BorrowingCreateSerializer
from borrowings.filters import BorrowingFilter
from notifications.tasks import send_telegram_notification


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        """
        Performs the creation of a borrowing, decrements book inventory,
        saves the borrowing, and sends a Telegram notification.
        """
        book = serializer.validated_data["book"]
        book.inventory -= 1
        book.save()
        borrowing = serializer.save(user=self.request.user) # NEW: Store the saved instance

        # --- NEW: Telegram Notification Logic ---
        # Construct the message for the notification
        message = (
            f"New borrowing created:\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        # Send the notification asynchronously using Celery
        send_telegram_notification.delay(message)
        # --- END NEW: Telegram Notification Logic ---

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        read_serializer = BorrowingReadSerializer(instance=serializer.instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        url_name="return-borrowing",
    )
    def return_borrowing(self, request, pk=None):
        """
        Handles the return of a borrowed book.
        Sets the actual return date and increments the book's inventory.
        """
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now().date()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
