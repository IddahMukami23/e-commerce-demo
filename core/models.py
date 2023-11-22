from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userAuth.models import User
from taggit.managers import TaggableManager

STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Drafted'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    (1, '✦✧✧✧✧'),
    (2, '✦✦✧✧✧'),
    (3, '✦✦✦✧✧'),
    (4, '✦✦✦✦✧'),
    (5, '✦✦✦✦✦'),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.


class Category(models.Model):
    cid = ShortUUIDField(length=10, max_length=30, prefix='cat', alphabet='abcdefg1234', unique=True)
    title = models.CharField(max_length=100, default='Fruits and Vegetables')
    image = models.ImageField(upload_to='user_directory_path', default='category.jpg')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<image src="%s" width="50" height="50"/>' % self.image.url)

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(length=10, max_length=30, prefix='ven', alphabet='abcdefg1234', unique=True)
    title = models.CharField(max_length=100, default='Fruity')
    image = models.ImageField(upload_to='user_directory_path', default='vendor.jpg')
    cover_image = models.ImageField(upload_to='user_directory_path', default='vendor.jpg')
    description = models.TextField(null=True, blank=True, default='I am an amazing vendor')

    address = models.CharField(max_length=100, default='254 Nairobi.')
    contact = models.CharField(max_length=100, default='+254 (567) 890')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_resp_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<image src="%s" width="50" height="50"/>' % self.image.url)

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(length=10, max_length=30, prefix='prod', alphabet='abcdefg1234', unique=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='product')

    title = models.CharField(max_length=100, default='Fresh fruit')
    image = models.ImageField(upload_to='user_directory_path', default='product.jpg')
    description = models.TextField(null=True, blank=True, default='Uploaded product')

    price = models.DecimalField(max_digits=65, decimal_places=2, default='1.99')
    old_price = models.DecimalField(max_digits=65, decimal_places=2, default='2.99')

    specifications = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default='Organic', null=True, blank=True)
    stock_count = models.CharField(max_length=100, default=10, null=True, blank=True)
    life = models.CharField(max_length=100, default='7 Days', null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)

    sku = ShortUUIDField(length=10, max_length=30, prefix='sku', alphabet='abcdefg1234', unique=True)

    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<image src="%s" width="50" height="50"/>' % self.image.url)

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='user_directory_path', default='product.jpg')
    product = models.ForeignKey(Product, related_name='p_images',  on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


class CartOrder(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=65, decimal_places=2, default='1.99')
    paid_stats = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='processing')

    class Meta:
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qtty = models.CharField(max_length=100, default=0)
    price = models.DecimalField(max_digits=65, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=65, decimal_places=2, default='1.99')

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def product_image(self):
        return mark_safe('<image src="/media/%s" width="50" height="50"/>' % self.image)


class ProductReview(models.Model):
    user = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
