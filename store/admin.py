from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Collection, Product, Customer, Order, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_display = [
        "title",
        "unit_price",
        "inventory_status",
        "collection_title",
    ]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 50
    list_select_related = ["collection"]
    search_fields = ["title"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS,
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    ordering = ["user__first_name", "user__last_name"]
    list_per_page = 20
    list_select_related = ["user"]
    list_editable = ["membership"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(orders_count=Count("order"))
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "customer_name"]
    ordering = ["-placed_at"]
    list_select_related = ["customer"]

    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html(
            '<a href="{}">{}</a>', url, collection.products_count
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(products_count=Count("product"))
        )


# admin.site.register(Product, ProductAdmin)
# admin.site.register(Customer, CustomerAdmin)
