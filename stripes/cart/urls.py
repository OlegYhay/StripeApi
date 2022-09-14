from django.urls import path

# from books.views import OrderCreate, OrderCreated
from .views import cart_detail, cart_add, cart_remove
app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    # path('create_order/', OrderCreate.as_view(), name='create_order'),
    # path('create_order/success/', OrderCreated.as_view(), name='created_order'),
]
