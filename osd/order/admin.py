from django.contrib import admin
from .models import Order, OrderDetail

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
    list_display = ['order_id', 'cus_id', 'ship_address', 'order_date']
    list_display_links = ('order_id', 'cus_id')
    search_fields = ['order_id', 'cus_id', 'ship_address']
    readonly_fields = ['order_id', 'cus_id', 'total', 'ship_address', 'order_date', 'total',
                       'status','discount', 'freight', 'tax']
    fieldsets = [
        ('ORDER INFORMATION',{'fields':['order_id', 'order_date', 'status']}),
        ('BILLING INFORMATION',{'fields':['cus_id', 'total', 'discount', 'freight', 'tax']}),
        ('SHIPPING INFORMATION',{'fields':['ship_address']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

