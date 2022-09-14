from django.forms import forms, ModelForm

from items.models import Order, Discount


class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        fields = ['coupon', ]


