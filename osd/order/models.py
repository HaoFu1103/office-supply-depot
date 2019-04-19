from django.db import models

# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Order Total')
    ship_address = models.CharField(max_length=250, blank=False)
    order_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-order_date']

    def __str__(self):
        return str(self.order_id)

class OrderDetail(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderDetail'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
