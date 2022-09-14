from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from items.models import Items
from .cart import Cart
from .forms import CardAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    form = CardAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=1,
                 update_quantity=cd['update'])
        return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    product_ids = cart.cart.keys()  # получение всех ключей книг
    products = Items.objects.filter(id__in=product_ids)  # получение книг из бд
    sum = 0
    for product in products:  # Обход книг из бд
        cart.cart[str(product.id)]['product'] = product
        cart.cart[str(product.id)]['total_price'] = float(cart.cart[str(product.id)]['quantity']) * float(
            cart.cart[str(product.id)]['price'])
        sum += cart.cart[str(product.id)]['total_price']
    return render(request, 'cart/cart_detail.html', {'cart': cart.cart, 'itogsumm': sum,'counts':products.count()})
