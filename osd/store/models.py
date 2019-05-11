from django.db import models
from django.urls import reverse
from PIL import Image
from django.core.validators import MinValueValidator #to validate minimum value
from decimal import *


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    # to add options to model (https://docs.djangoproject.com/en/dev/topics/db/models/#meta-options)
    class Meta:
        ordering = ('name',)
        verbose_name ='category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('store:products_by_category', args=[self.slug])

    # to create  human readable representation
    def __str__(self):
        return '{}'.format(self.name)

# slug used for url (e.g. http://localhost/store/golf-umbrella -> golf-umbrella is a slug for product name Golf Umbrella)
class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price =  models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to='product',blank=True) # image uploaded to a folder called product
    weight = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name ='product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('store:ProdCatDetail', args=[self.category.slug, self.slug])

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        output_size = (500, 500)
        img.thumbnail(output_size)
        img.save(self.image.path)
