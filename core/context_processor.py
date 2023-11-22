from core.models import (Product, Category, Vendor, ProductReview, ProductImages, Wishlist, CartOrder, CartOrderItems,
                         Address)


def default(request):
    categories = Category.objects.all()
    # address = Address.objects.get(user=request.user)
    return {
        'categories': categories,
        # 'address': address
    }
