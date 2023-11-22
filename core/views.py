from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.models import (Product, Category, Vendor, ProductReview, ProductImages, Wishlist, CartOrder, CartOrderItems,
                         Address)


# Create your views here.
def home(request):
    products = Product.objects.filter(featured=True, product_status='published').order_by('-id')

    context = {
        'products': products
    }
    return render(request, 'core/index.html', {'products': products})


def shop_list(request):
    products = Product.objects.filter(product_status='published').order_by('-id')

    context = {
        'products': products
    }
    return render(request, 'core/shop.html', {'products': products})


def category_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'core/category.html', {'categories': categories})


def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        'category': category,
        'products': products

    }

    return render(request, 'core/category_list.html', {'category': category, 'products': products})


def vendor_display(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendors.html', {'vendors': vendors})


def vendor_list_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')

    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'core/vendors_list.html', context)


def product_details_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    p_images = product.p_images.all()

    context = {
        'p': product,
        'p_images': p_images,
        'products': products,
    }
    return render(request, 'core/detail.html', context)
