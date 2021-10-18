from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from store.models import Product, OrderItem


def say_hello(request):
    products = Product.objects.filter(
        Q(inventory__lt=10) | ~Q(unit_price__lt=10)
    )

    query_set = Product.objects.filter(
        id__in=OrderItem.objects.values("product__id").distinct()
    ).order_by("title")

    return render(
        request,
        "index.html",
        {"products": list(query_set), "queryset": list(products)},
    )
