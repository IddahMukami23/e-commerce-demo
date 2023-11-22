from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    path('product_list/', views.shop_list, name='shop'),
    path('product_detail/<pid>/', views.product_details_view, name='details'),

    path('category/', views.category_view, name='category'),
    path('category_list/<cid>/', views.category_product_list, name='category_product_list'),

    path('vendor/', views.vendor_display, name='vendor'),
    path('vendor_details/<vid>/', views.vendor_list_view, name='vendor_details'),

]
