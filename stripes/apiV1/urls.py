from django.urls import path

from apiV1.views import ItemRetrieveApiView, ItemBuyRetrieveApiView, SuccessTemplateView, CancelTemplateView, \
    ListItemBuyView, PaymentCreateIntent, PaymentListCreateIntent

urlpatterns = [
    path('item/<int:pk>', ItemRetrieveApiView.as_view(), name='item'),
    path('buy/<int:pk>', ItemBuyRetrieveApiView.as_view(), name='buy_item'),
    path('buy/group/<int:pk>', ListItemBuyView.as_view(), name='buy_group'),
    path('buy/intent/<int:pk>', PaymentCreateIntent.as_view(), name='buy_item_intent'),
    path('buy/intent/group/<int:pk>', PaymentListCreateIntent.as_view(), name='buy_list_intent'),
    path('buy/success/', SuccessTemplateView.as_view(), name='success'),
    path('buy/cancel/', CancelTemplateView.as_view(), name='cancel'),
]
