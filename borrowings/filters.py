from django_filters import rest_framework as filters
from borrowings.models import Borrowing


class BorrowingFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(method="filter_by_active")

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    def filter_by_active(self, queryset, name, value):
        if value:
            return queryset.filter(actual_return_date__isnull=True)
        return queryset.filter(actual_return_date__isnull=False)
