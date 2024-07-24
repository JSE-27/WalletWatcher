# walletwatcher/urls.py

from django.urls import path
from .views import WalletTransactionsAPIView, DummyTransaction

urlpatterns = [
    path('transaction', WalletTransactionsAPIView.as_view(), name='wallet-transactions'),
    path('make-transaction', DummyTransaction.as_view(), name='wallet-transactions'),
]
