from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    path('product_list/', views.shop_list, name='shop'),
    path('product_detail/<pid>/', views.product_details_view, name='details'),

    path('category/', views.category_view, name='category'),
    path('category_list/<cid>/', views.category_product_list, name='category_product_list'),

    path('vendor/', views.vendor_display, name='vendor'),
    path('vendor_details/<vid>/', views.vendor_list_view, name='vendor_details'),

    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),


    path('add_review/<pid>/', views.ajax_add_review, name='add-review'),

    path('search/', views.search_view, name='search'),

    path('filter-products/', views.filter_product, name='filter-product'),


    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    path('update-cart/', views.update_cart, name='update-cart'),


    path('checkout/', views.checkout_view, name='checkout'),

    path('payment/', views.payment, name='payment'),
    # path('mpesa/', views.mpesa, name='mpesa'),




]
