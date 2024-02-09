import django.contrib.auth.models
from django.shortcuts import render
from store.models import Customer, Order, OrderItem, Product

# Create your views here.


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/Store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}

    context = {"items": items, "order": order}
    return render(request, "store/Cart.html", context)


def checkout(request):
    """
    first I have to get the orderitems to render to the template
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
    context = {"order": order, "items": items}
    return render(request, "store/Checkout.html", context)
