# books/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from books.models import Book


class CoverListFilter(admin.SimpleListFilter):
    title = _('Cover type')
    parameter_name = 'cover'

    def lookups(self, request, model_admin):
        return (
            ('HARD', _('Hardcover')),
            ('SOFT', _('Softcover')),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cover=self.value())


class InventoryRangeFilter(admin.SimpleListFilter):
    title = _('Inventory range')
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return (
            ('0', _('Out of stock')),
            ('1-10', _('Low stock (1-10)')),
            ('10+', _('In stock (10+)')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(inventory=0)
        elif self.value() == '1-10':
            return queryset.filter(inventory__range=(1, 10))
        elif self.value() == '10+':
            return queryset.filter(inventory__gt=10)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'cover_type',
        'inventory_status',
        'daily_fee',
        'created_at',
    )
    list_display_links = ('title', 'author')
    list_filter = (CoverListFilter, InventoryRangeFilter)
    search_fields = ('title', 'author')
    ordering = ('title',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'author')
        }),
        (_('Inventory Info'), {
            'fields': ('cover', 'inventory', 'daily_fee')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['restock_books']

    @admin.display(description=_('Cover type'))
    def cover_type(self, obj):
        return dict(Book.CoverChoices.choices).get(obj.cover)

    @admin.display(description=_('Inventory status'))
    def inventory_status(self, obj):
        if obj.inventory == 0:
            return _('Out of stock')
        elif obj.inventory < 5:
            return _('Low stock')
        return _('In stock')

    @admin.action(description=_('Restock selected books'))
    def restock_books(self, request, queryset):
        updated = queryset.update(inventory=10)
        self.message_user(
            request,
            _('Successfully restocked %(count)d books') % {'count': updated}
        )
