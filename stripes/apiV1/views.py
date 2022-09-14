import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apiV1.serializers import ItemsSerializer, OrdersSerializer
from cart.cart import Cart
from items.models import Items, Order
import stripe

stripe.api_key = settings.STRIP_SECRET_KEY


class ItemRetrieveApiView(RetrieveAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'item': self.object}, template_name='item_template.html')


class ItemsListApiView(ListAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.objects = self.get_queryset()
        return Response({'items': self.objects}, template_name='main.html')


class ItemBuyRetrieveApiView(APIView):
    def get(self, request, *args, **kwargs):
        item = Items.objects.get(id=self.kwargs["pk"])
        MY_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(str(item.price) + "00"),
                },
                'quantity': 1,
            }],
            mode='payment',
            allow_promotion_codes=True,
            success_url=MY_DOMAIN + '/buy/success/',
            cancel_url=MY_DOMAIN + '/buy/cancel/',
        )
        return redirect(checkout_session.url)


class ListItemBuyView(APIView):
    def get(self, request, *args, **kwargs):
        cart = self.get_cart()
        items = cart['cart']
        line_items = []
        order = Order.objects.get(pk=self.kwargs['pk'])

        # tax
        taxs = []
        if order.tax != None and order.tax.tax > 0:
            taxs = stripe.TaxRate.create(
                display_name="Налог",
                inclusive=False,
                percentage=order.tax.tax,
                country="RU",
            )
            taxs = [taxs['id'], ]

        # create products
        for key, value in items.items():
            if value['product'].currency == 'usd':
                value['price'] = int(value['price']) * 61
            elif value['product'].currency == 'eur':
                value['price'] = int(value['price']) * 81
            line_items.append({
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': value['product'],
                    },
                    'unit_amount': int(str(value['price']) + "00"),
                },
                'quantity': value['quantity'],
                'tax_rates': taxs,
            })
        MY_DOMAIN = "http://127.0.0.1:8000"

        # discount
        coupon = None
        if order.discount != None and order.discount.sale > 0:
            coupon = stripe.Coupon.create(percent_off=order.discount.sale, duration="once")

        # create stripe session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            discounts=[{'coupon': coupon, }],
            success_url=MY_DOMAIN + '/buy/success/',
            cancel_url=MY_DOMAIN + '/buy/cancel/',
        )

        # delete cart
        cart = Cart(self.request)
        cart.clean()
        return redirect(checkout_session.url)

    def get_cart(self):
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Items.objects.filter(id__in=products_ids)
        sum = 0
        for product in products:
            cart.cart[str(product.id)]['product'] = product
            cart.cart[str(product.id)]['total_price'] = float(cart.cart[str(product.id)]['quantity']) * float(
                cart.cart[str(product.id)]['price'])
            sum += cart.cart[str(product.id)]['total_price']
        return {'cart': cart.cart, 'itogsumm': sum}


class PaymentCreateIntent(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        item = Items.objects.get(pk=self.kwargs['pk'])
        print(item)
        stripes = stripe.PaymentIntent.create(
            amount=int(str(item.price) + "00"),
            currency=item.currency,
            payment_method_types=[
                "card"
            ],
        )
        return Response({'client_secret': stripes.client_secret,
                         'itogsumm': str(item.price)+' '+ item.currency}, template_name='checkout.html')


class PaymentListCreateIntent(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        cart = self.get_cart()
        stripes = stripe.PaymentIntent.create(
            amount=int(str(int(cart['itogsumm'])) + "00"),
            currency='rub',
            payment_method_types=[
                "card"
            ],
        )
        cartic = Cart(self.request)
        cartic.clean()
        return Response({'client_secret': stripes.client_secret,
                         'itogsumm': str(cart['itogsumm'])+' rub'}, template_name='checkout.html')

    def get_cart(self):
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Items.objects.filter(id__in=products_ids)
        sum = 0
        for product in products:
            cart.cart[str(product.id)]['product'] = product
            if product.currency == 'usd':
                cart.cart[str(product.id)]['price'] = int(cart.cart[str(product.id)]['price']) * 61
            elif product.currency == 'eur':
                cart.cart[str(product.id)]['price'] = int(cart.cart[str(product.id)]['price']) * 81
            cart.cart[str(product.id)]['total_price'] = float(cart.cart[str(product.id)]['quantity']) * float(
                cart.cart[str(product.id)]['price'])
            sum += cart.cart[str(product.id)]['total_price']
        return {'cart': cart.cart, 'itogsumm': sum}


class SuccessTemplateView(TemplateView):
    template_name = 'payment/success.html'


class CancelTemplateView(TemplateView):
    template_name = 'payment/cancel.html'
