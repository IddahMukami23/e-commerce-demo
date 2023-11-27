from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import (Product, Category, Vendor, ProductReview, ProductImages, Wishlist, CartOrder, CartOrderItems,
                         Address)
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.template.loader import render_to_string


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

    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    review_form = ProductReviewForm()

    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    p_images = product.p_images.all()

    context = {
        'p': product,
        'p_images': p_images,
        'products': products,
        'reviews': reviews,
        'make_review': make_review,
        'review_form': review_form

    }
    return render(request, 'core/detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        'products': products,
        'tag': tag,

    }
    return render(request, 'core/tag.html', context)


def ajax_add_review(request, pid):
    if request.method == 'POST':
        product = Product.objects.get(pid=pid)
        user = request.user

        review_text = request.POST.get('review', '')
        rating_value = request.POST.get('rating', '')

        if review_text and rating_value:
            review = ProductReview.objects.create(
                user=user,
                product=product,
                review=review_text,
                rating=rating_value,
            )

            context = {
                'user': user.username,
                'review': review_text,
                'rating': rating_value,
            }

            return JsonResponse({'bool': True, 'context': context})

    return JsonResponse({'bool': False, 'error': 'Invalid POST data'})


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains=query).order_by('-date')

    context = {
        'products': products,
        'query': query
    }

    return render(request, 'core/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    products = Product.objects.filter(product_status='published').order_by('-id').distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string('core/async/product_filter.html', {'products': products})
    return JsonResponse({'data': data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qtty': request.GET['qtty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qtty'] = int(cart_product[str(request.GET['id'])]['qtty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({'data': request.session['cart_data_obj'],
                         'totalcartitems': len(request.session['cart_data_obj'])})
