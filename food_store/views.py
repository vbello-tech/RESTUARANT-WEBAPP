from django.shortcuts import render
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, View, ListView
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import *
from accounts.models import *
from .forms import *
import random, string, io
#from main.settings import Publishable_key, Secret_key
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
#from accounts.models import Userprofile
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# HOME PAGE VIEW
class HomeView(View):
    def get(self, *args, **kwargs):
        foods = Food.objects.order_by('-created_date')[:8]
        context = {
            'foods': foods,
        }

        return render(self.request, "food_store/home.html", context)


# about page view
class AboutView(TemplateView):
    template_name = "food_store/about.html"


# VIEW TO DISPLAY ALL FOOD IN MODELS
class FoodListView(ListView):
    model = Food
    paginate_by = 5
    context_object_name = "foods"
    template_name = "food_store/food_list.html"

    #QUERYSET TO ORDER ALL FOOD ACCORDING TO THIER CREATED DATE
    def get_queryset(self):
        return Food.objects.order_by('-created_date')


# DETAIL VIEW FOR EACH FOOD ITEM
def ProductView(request, pk):
    food = Food.objects.get(pk=pk)
    context = {
        'food': food
    }
    return render(request, 'food_store/food_detail.html', context)


# FUNCTION TO ADD ITEM TO CART
@login_required
def add_to_cart(request, pk):
    # ORDER ITEM TO BE ADDED TO CART
    food = get_object_or_404(Food, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        food=food,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # IF STATEMENT TO CHECK IF ORDER ITEM EXIST IN CART
    if order_qs.exists():
        order = order_qs[0]
        # IF STATEMENT TO INCREASE THE ORDER ITEM QUANTITY BY 1 IF THE USER ALREADY HAS THE food ITEM IN CART
        if order.foods.filter(food__pk=food.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was increased.")
        else:
            order.foods.add(order_item)
            return redirect('food:food_detail', pk=pk)
    else:
        # CREATE AN ORDER ITEM OF FOOD IF IT DOES NOT EXIST IN USER CART
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.foods.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('food:food_detail', pk=pk)


# FUNCTION TO ADD ITEM TO CART
@login_required
def add_to_cart_item(request, pk):
    # ORDER ITEM TO BE ADDED TO CART
    food = get_object_or_404(Food, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        food=food,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # IF STATEMENT TO CHECK IF ORDER ITEM EXIST IN CART
    if order_qs.exists():
        order = order_qs[0]
        # IF STATEMENT TO INCREASE THE ORDER ITEM QUANTITY BY 1 IF THE USER ALREADY HAS THE food ITEM IN CART
        if order.foods.filter(food__pk=food.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was increased.")
        else:
            order.foods.add(order_item)
            return redirect('food:order_summary')
    else:
        # CREATE AN ORDER ITEM OF FOOD IF IT DOES NOT EXIST IN USER CART
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.foods.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('food:order_summary')


# REMOVE FROM CART FUNCTIONS
@login_required
def remove_from_cart(request, pk):
    # ORDER ITEM TO REMOVE FROM CART
    food = get_object_or_404(Food, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    # CHECK IF ORDER ITEM EXIST IN CART ITEMS OF USER
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.foods.filter(food__pk=food.pk).exists():
            order_item = OrderItem.objects.filter(
                food=food,
                user=request.user,
                ordered=False
            )[0]
            # REMOVE FROM CART
            order.foods.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect( 'food:order_summary')
        else:
            return redirect( 'food:order_summary')
    else:
        return redirect( 'food:order_summary')

# FUNCTION TO REMOVE SINGLE ITEM FROM CART
@login_required
def remove_from_cart_item(request, pk):
    # CHECK IF ORDERED ITEM EXIST IN CART
    food = get_object_or_404(Food, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is in the order
        if order.foods.filter(food__pk=food.pk).exists():
            order_item = OrderItem.objects.filter(
                food=food,
                user=request.user,
                ordered=False
            )[0]
            # REDUCE QUANTITY OF ORDER ITEM BY 1
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "This item quantiy was reduced.")
            return redirect('food:order_summary')
        else:
            return redirect('food:order_summary')
    else:
        return redirect('food:order_summary')


# VIEW TO DISPLAY ALL AVAILABLE ORDER ITEM THAT THE ORDERED STATUS IS FALSE
class order_summaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order,
            }
            return render(self.request, 'food_store/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "ADD ITEMS TO YOUR CART")
            return redirect("food:food_list")


# CHECK OUT VIEW
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            # ALL AVAILABLE ORDER ITEM THAT HAS NOT BEEN PAID FOR
            order = Order.objects.get(user=self.request.user, ordered=False)
            # CHECK OUT FORM
            form = CheckOutForm()
            context = {
                'form': form,
                'couponform':CouponForm(),
                'DISPLAY_COUPON_FORM':True,
                'order':order
            }
        except ObjectDoesNotExist:
            return redirect("food:checkout")

        return render (self.request, 'food_store/check_out.html', context)

    def post(self, *args, **kwargs):
        try:
            # ALL ORDER ITEM TO CHECK OOUT
            order = Order.objects.get(user=self.request.user, ordered=False)
            # CHECK OUT FORM
            form = CheckOutForm(self.request.POST or None)
            #checkout = Checkout.objects.get(user=self.request.user)
            # GETTING THE USER ADDRESS AND PHONE NUMBER TO ADD TO ORDER
            if form.is_valid():
                address = form.cleaned_data.get('address')
                phone = form.cleaned_data.get('phone')
                #save_info = form.cleaned_data.get('save_info')
               # #use_saved_info = form.cleaned_data.get('use_saved_info')
                #if save_info:
                #    if checkout.exist():
                #        new_checkout_details = Checkout.objects.update(
                #            address = address,
                #            phone = phone
                #        )
                #    else:
                #        new_checkout_details = Checkout.objects.create(
                #            address=address,
                #            phone=phone
                #        )
                #    new_checkout_details.save()
                #if use_saved_info:
                #    if checkout.exist():
                #        billing_address = checkout.address
                #        billing_phone = checkout.phone
                #    else:
                 #       messages.warning(self.request, "YOU DONT HAVE A SAVED SHIPPING ADDRESS AND PHONE NUMBER.")
                 #       return redirect('food:checkout')
                #else:
                 #   billing_address = address
                #    billing_phone = phone

                order.billing_address = address #billing_address
                order.phone = phone #billing_phone
                order.save()
                # SENDING THE ORDER CONFIRMATION EMAIL
                #order_confirmation_email(self.request)
                messages.info(self.request, "ORDER SUCCESSFUL.")
                return redirect('food:payment')
            else:
                return redirect('food:checkout')

        except ObjectDoesNotExist:
            return redirect('food:checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        email = order.user.email
        context = {
            'order':order,
            'email':email,
        }
        return render (self.request, 'food_store/payment.html', context)

# FUNCTION TO GET COUPON
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return redirect('food:checkout')

# VIEW TO ADD COUPON TO AN ORDER
class AddCouponView(View):
    def post(self, *args, **kwargs):
        # COUPON FORM TO ENTER ANY AVAILABLE UNSED Coupon
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            # GET COUPON AND ADD TO THE ORDER
            try:
                code = form.cleaned_data.get('code')
                # ORDER THAT THE COUPON WILL BE ADDED TO
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.info(self.request, "COUPON ADDED SUCCESSFULLY.")
                return redirect("food:checkout")
            except ObjectDoesNotExist:
                return redirect("food:checkout")

# FUNCTION TO SEARCH FOR A FOOD ITEM
def search_food(request):
    if request.method =="POST":
        # THE VALUE TO BE SEARCH FROM THE FORM
        searched = request.POST['searched']
        # FILTER THE VALUE FOR THE DB
        food = Food.objects.filter(category = searched)
        context = {
            'searched':searched,
            'food':food
        }
        return render(request, 'food_store/search_food.html', context)
    else:
        return render(request, 'food_store/search_food.html')

# FUNCTION TO ASSIGN TABLE NUMBER TO USERS
def asign_table(request):
    # GET THE TIME OF THE USER RESERVATION
    time = request.POST['time']
    # VALUE TO STORE HOW MANY TIMES THE LOOP HAS RUN
    x = 0
    # WHILE LOOP TO ASIGN TABLE NUMBER
    while True:
        # RANDOMLY SELECT A TABLE NUMBER FROM 0 - 30
        table_number = random.randint(0, 31)
        # CHECK IF A RESERVATION FOR THE table_number ALREADY EXIST FOR THE USER SELECTED TIME
        check_table = Table.objects.filter(
            table_time = time,
            table_number = table_number,
            taken = True
        )
        x += 1
        # IF A RESERVATION FOR THE table_number ALREADY EXIST FOR THE USER SELECTED TIME, RUN WHILE LOOP AGAIN
        if check_table.exists == True and x <= 30 :
            continue
        # ASSIGN table_number IF IT DOES NOT EXIST FOR THE USER SELECTED TIME AND THE LOOP HAS RAN FOR LESS THAN 31 TIMES.
        elif check_table.exists != True and x <= 30:
            table = Table.objects.get_or_create(
                    table_time = time,
                    table_number = table_number,
                    taken = True
            )
            return int(table_number)
            break
        # RETURN FALSE IF LOOP HAS RAN FOR MORE THAN 30 TIMES SO USER CAN INPUT ANOTHER TIME TO SCHEDULE
        elif check_table.exist != True and x >= 30:
            return False
            break

# GENERATE RESERVATION CODE
def reservation_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# RESERVATION VIEW
class ReservationView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "food_store/reservations.html")
    def post(self, request, *args, **kwargs):
        # GET THE USER PREFERENCE FOR A RESERVTION
        if request.method =="POST":
            date = request.POST['date']
            time = request.POST['time']
            persons = request.POST['persons']
            table = asign_table(request)
            # IF THE asign_table function returns a value create a reservation for user in db
            if table:
                reservation, created = Reservation.objects.get_or_create(
                        date = date,
                        time = time,
                        persons = persons,
                        booker = request.user,
                        table = table,
                        booked = True,
                        reservation_code = reservation_code()
                )
            else:
                # if asign_table function returns false redirect back to reservation page to reslect another time for reservation
                if table == False:
                    messages.warning(self.request, "THERE IS NO AVAILABLE TABLE FOR YOUR TIME PLS CHECK BACK LATER OR SELECT ANOTHER TIME")
                    return redirect('food:reserve')
            return redirect('food:reserved',  pk=reservation.pk)
        else:
            return redirect('food:reserve')

# view function to display user reservation with reservation details
def reservation_confirm(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    messages.info(request, "RESERVATION SUCCESSFUL.")
    context = {
        'item':reservation
    }
    return render(request, 'food_store/reservation_confirm.html', context)


def handler404(request, exception):
    context = {"<h1>PAGE NOT FOUND!! ARE YOU SURE YOU ARE NAVIGATING TO THE RIGHT PAGE?</h1>"}
    response = render(request, "Templates/404.html", context)
    response.status_code = 404
    return response


def handler500(request):
    context =  {"<h1>OOPS !!! <br> SEVER ERROR!!! <br> </h1>"}
    response = render(request, "Templates/500.html", context)
    response.status_code = 500
    return response