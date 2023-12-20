from django.urls import path

from . import views
urlpatterns = [
    path("checkout/", views.MpesaCheckout.as_view(), name="checkout"),
    path("callback/", views.MpesaCallBack.as_view(), name="callback"),
    path("check_transaction_status/", views.CheckTransactionStatus.as_view(),
         name="check_transaction_status"),
]
