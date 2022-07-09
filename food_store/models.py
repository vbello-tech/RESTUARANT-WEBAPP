from django.db import models

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str_(self):
        return self.category

# get each category and display as a chioce
#cat = Category.objects.all().values_list('category', 'category')
#CATEGORY_CHOICES = []
#for choice in cat:
 #   CATEGORY_CHOICES.append(choice)

CATEGORY_CHOICES = (
    ('Local Delicacies', 'Local Delicacies'),
    ('Foriegn Delicacies', 'Foriegn Delicacies'),
    ('Medicinal Drinks', 'Medicinal Drinks'),
    ('Wines & Alcohol', 'Wines & Alcohol')
)

LABEL_CHOICES = (
    ('Local Delicacies', 'Local Delicacies'),
    ('Foriegn Delicacies', 'Foriegn Delicacies'),
    ('Medicinal Drinks', 'Medicinal Drinks'),
    ('Wines & Alcohol', 'Wines & Alcohol')
)

# models for each food item
class Food(models.Model):
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    img = models.ImageField(upload_to="FOOD/", blank=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=750)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dis_price = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=10)
    label = models.CharField(choices=LABEL_CHOICES, blank=True, null=True, max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey('auth.user',  on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.food.price

    def get_total_discount_price(self):
        return self.quantity * self.food.dis_price

    def get_final_price(self):
        if self.food.dis_price:
            return self.get_total_discount_price()
        return self.get_total_price()

    def __str__(self):
        return f"{self.quantity} of {self.food.name}"



    
class Order(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    order_code = models.CharField(max_length=20, blank=True, null=True)
    foods = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def total_price(self):
        total = 0
        for order_item in self.foods.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.price
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    price = models.DecimalField(blank=True, default=00.00, decimal_places=2, max_digits=10)
    def __str__(self):
        return self.code



# MODELS FOR RESERVATION
class Reservation(models.Model):
    booker = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    time = models.CharField(max_length=20, blank=False)
    persons = models.IntegerField(default=1)
    booked = models.BooleanField(default=False)
    table = models.IntegerField(blank=True, null=True)
    reservation_code = models.CharField(max_length=20, blank=True, null=True)
    booked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booker}"

# models to store reserved table
class Table (models.Model):
    table_number = models.IntegerField()
    table_time = models.CharField(max_length=20)
    taken = models.BooleanField(default=False)
