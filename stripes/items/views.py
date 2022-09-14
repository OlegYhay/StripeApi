from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from cart.cart import Cart
from items.models import Order, Items


class OrderCreateView(CreateView):
    model = Order
    fields = ['discount', 'tax']
    template_name = 'order_create.html'

    def get_success_url(self):
        if self.request.POST['varia'] == 'session':
            return reverse('buy_group', kwargs={'pk': self.pk})
        else:
            return reverse('buy_list_intent', kwargs={'pk': self.pk})

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        cart = self.get_cart()
        items = cart['cart']
        for key, value in items.items():
            print(value['product'])
            fields.item.add(value['product'])
        fields.total = cart['itogsumm']
        fields.save()
        self.pk = fields.pk;
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        data = super(OrderCreateView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Items.objects.filter(id__in=products_ids)
        sum = 0
        info = self.get_cart()
        data['cart'] = info['cart']
        data['itogsumm'] = info['itogsumm']
        return data

    def get_cart(self):
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Items.objects.filter(id__in=products_ids)
        sum = 0
        currency = []
        for product in products:
            cart.cart[str(product.id)]['product'] = product
            cart.cart[str(product.id)]['total_price'] = float(cart.cart[str(product.id)]['quantity']) * float(
                cart.cart[str(product.id)]['price'])
            if currency.count(product.currency):
                currency.append(product.currency)
            sum += cart.cart[str(product.id)]['total_price']
        multi = False
        if len(currency) > 1:
            multi = True
        return {'cart': cart.cart, 'itogsumm': sum, 'multi': multi}
