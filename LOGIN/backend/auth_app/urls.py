from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.get_users, name='get_users'),
    path('users/<str:username>/', views.delete_user, name='delete_user'),
    
    path('products/', views.get_products, name='get_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/', views.get_user_orders, name='get_user_orders'),
    path('orders/<str:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('load_order/', views.load_order, name='load_order'),
    path('get-orders/', views.get_orders, name='get_orders'),
    path('update_item/', views.update_item, name='update_item'),  # ✅ This must be here
] 