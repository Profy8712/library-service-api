from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from books.models import Book
from users.models import User
from borrowings.models import Borrowing


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "cover", "inventory", "daily_fee")
    list_filter = ("cover",)
    search_fields = ("title", "author")
    fieldsets = (
        (None, {"fields": ("title", "author")}),
        (
            "Inventory Info",
            {
                "fields": (
                    "cover",
                    "inventory",
                    "daily_fee",
                )
            },
        ),
    )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    )
    list_filter = ("borrow_date", "expected_return_date")
    search_fields = (
        "book__title",
        "user__email",
    )
    raw_id_fields = ("book", "user")
    date_hierarchy = "borrow_date"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "book",
                    "user",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "borrow_date",
                    "expected_return_date",
                    "actual_return_date",
                )
            },
        ),
    )
