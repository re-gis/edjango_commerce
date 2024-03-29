import json
import django.contrib.auth.models
from django.shortcuts import render
from store.models import Customer, Order, OrderItem, Product, ShippingAddress
from django.http import JsonResponse
import datetime

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/Store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/Cart.html", context)


def checkout(request):
    """
    first I have to get the orderitems to render to the template
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order
    context = {"order": order, "items": items, "cartItems": cartItems}
    return render(request, "store/Checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("item added successfully", safe=False)


def prodessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
            )
    else:
        print("User is not authenticated")
    return JsonResponse("Payment submitted successfully", safe=False)
