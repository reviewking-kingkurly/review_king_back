from django.db import models

from core.models import TimeStampModel

class MainCategory(models.Model): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = "main_categories"

class SubCategory(models.Model): 
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    name          = models.CharField(max_length=45)

    class Meta: 
        db_table = "sub_categories"

class Product(TimeStampModel): 
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    name         = models.CharField(max_length=50)
    group        = models.CharField(max_length=50)
    price        = models.DecimalField(max_digits=10, decimal_places=0)
    thumbnail    = models.URLField(max_length=300)

    class Meta: 
        db_table = "products"

class ProductImage(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    img_url = models.URLField(max_length=300)

    class Meta: 
        db_table = "product_images"

class OrderStatus(models.Model): 
    status = models.CharField(max_length=20)

    class Meta: 
        db_table = "order_statuses"

class Order(models.Model): 
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    order_num    = models.IntegerField()
    ordered_at   = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = "orders"

class OrderedItem(models.Model): 
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta: 
        db_table = "ordered_items"

class Delivery(models.Model): 
    ordered_item   = models.ForeignKey('OrderedItem', on_delete=models.CASCADE)
    delievery_date = models.DateField()