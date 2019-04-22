from django.contrib import admin
from .models import Order, OrderDetail, Routing
from django.db.models import Count, Sum, Min, Max

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

        response.context_data['summary'] = list(
            qs
            .all()
        )



        # TODO: make a list of dict (id, address)
        # select the first place as start, calculate time with every other address. pick the closest one

        return response