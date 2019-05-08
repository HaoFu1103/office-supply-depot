from django.contrib import admin
from .models import Order, OrderDetail, Routing
from django.db.models import Count, Sum, Min, Max
from .routing import calculate_best_routes

# Register your models here.
class OrderItemAdmin(admin.TabularInline):
    model = OrderDetail
    fieldsets = [
    ('Product',{'fields':['product']}),
    ('Quantity',{'fields':['quantity']}),
    ('Price',{'fields':['price']}),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0
    template = 'admin/order/tabular.html'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'ship_address', 'order_date']
    list_display_links = ['order_id']
    search_fields = ['order_id', 'ship_address']
    readonly_fields = ['order_id', 'total', 'ship_address', 'order_date', 'total']
    fieldsets = [
        ('ORDER INFORMATION',{'fields':['order_id', 'order_date']}),
        ('BILLING INFORMATION',{'fields':['total']}),
        ('SHIPPING INFORMATION',{'fields':['ship_address']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

@admin.register(Routing)
class RoutingAdmin(admin.ModelAdmin):
    change_list_template = 'admin/order/routing.html'
    date_hierarchy = 'order_date'

    def changelist_view(self, request, extra_context=None):
        response = super(RoutingAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        queried_set = list(qs.all())

        list_of_addresses = []
        for row in queried_set:
            lst = [row.order_id, row.ship_address]
            list_of_addresses.append(lst)

        ordered_set, origin_warehouse = calculate_best_routes(list_of_addresses)
        print(origin_warehouse)
        response.context_data['origin_warehouse'] = origin_warehouse
        list_of_sorted_addresses = []
        for curr_id in ordered_set:
            list_of_sorted_addresses.append(qs.get(order_id=curr_id))

        response.context_data['optimal_routes'] = list_of_sorted_addresses

        return response