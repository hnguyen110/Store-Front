from django.contrib import admin
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('<10', 'Low')]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    @staticmethod
    def thumbnail(instance):
        print(instance)
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" height=100 />')
        return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

    @staticmethod
    def collection_title(product):
        return product.collection.title

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_products = queryset.update(inventory=0)
        self.message_user(request, f'{updated_products} product(s) updated successfully')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = f'{reverse("admin:store_order_changelist")}?{urlencode({"customer__id": customer.id})}'
        return format_html(f'<a href="{url}">{customer.order_count} Order(s)</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('order'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    list_select_related = ['customer']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = f'{reverse("admin:store_product_changelist")}?{urlencode({"collection__id": collection.id})}'
        return format_html(f'<a href="{url}">{collection.product_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))
