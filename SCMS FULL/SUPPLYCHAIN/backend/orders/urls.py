from django.urls import path
from orders import views

urlpatterns = [
    path('load_order/', views.load_order, name='load_order'),
    path('get-orders/', views.get_orders, name='get_orders'),
    path('update_item/', views.update_item, name='update_item'),  # ✅ This must be here
]
