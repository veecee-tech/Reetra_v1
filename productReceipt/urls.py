from django.urls import path
from productReceipt.views import *

app_name = 'productReceipt'

urlpatterns = [
    path('add/', generate_receipt, name="gen_receipt"),
    path('delete_single/<int:id>/', delete_single_item, name="delete_item"),
    path('update/<int:id>/', update_item, name="update_item"),
    path('all_invoice/', all_invoice, name="all_invoice"),
    path('today/', printed_today, name='today'),
    path('this_week/', printed_this_week, name='this_week'),
    path('this_month/', printed_this_month, name='this_month'),
    path('receipt/<int:id>/<str:receipt_no>/', single_invoice, name='single_invoice'),
    path('add_item/<str:receipt_no>/', add_items, name="add_item"),
    path('all_items/<str:receipt_no>/', receipt_items, name="all_items"),
    path('approve/<int:id>/', approve, name='approve'),
    path('search/', search, name='search'),
]
