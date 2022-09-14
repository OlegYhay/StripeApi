from django import forms

from items.models import Discount

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CardAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

