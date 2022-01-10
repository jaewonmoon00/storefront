from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import reverse_related

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    #start_date and end_date
    # product_set field is created to return all the products under this promotion
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # To avoid CIRCULAR DEPENDANCY @@@@@@@@ this part I didn't know before
    # use this if you really have to because 'product' doesnt change even if you update the class name Product to something else
    # Related_name + prevents django from creating reverse relationship
    featured_product = models.ForeignKey('Product', on_delete=SET_NULL, null=True, related_name='+')
    def __str__(self):
        return self.title
    # set default ordering
    class Meta:
        ordering = ['title']
class Product(models.Model):
    # if primary_key is true, django will not automatically create primary_key for you
    # sku = models.CharField(max_length=10, primary_key=True)
    slug = models.SlugField(default='-')# search engine optimization
    title = models.CharField(max_length=255)
    description = models.TextField()
    #9999.99
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=PROTECT)
    # many to many relationship => this creates product_set field in Promotion class
    # you can change the default product_set name to wtv you want such as products
    promotions = models.ManyToManyField(Promotion) #, related_name='products')
    def __str__(self):
        return self.title
    # set default ordering
    class Meta:
        ordering = ['title']
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    """ # to customize database schema
    class Meta:
        db_table = 'store_customers'
        # to speed up queries
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]
    """

    def __str__(self):
        # look for what f does
        return f'{self.first_name} {self.last_name}'

    # for default sorting
    class Meta:
        ordering = ['first_name', 'last_name']

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    # if you accidently delete customer, it doesn't delete orders
    customer = models.ForeignKey(Customer, on_delete=PROTECT)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    #zip = models.CharField(max_length=255)

    # set primary_key True is important for OneToOneField
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    # Options: CASCADE, SET_NULL, PROTECT
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
# what is this class for?
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=PROTECT)
    product = models.ForeignKey(Product, on_delete=PROTECT)
    quantity = models.PositiveSmallIntegerField()
    # define unit_price here again even though we defined in product to make sure
    # the updated price is being updated
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)