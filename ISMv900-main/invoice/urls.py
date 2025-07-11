from django.urls import path
from .views import *
from invoice.views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'invoice'

urlpatterns = [
    # API endpoints
    path("api/havaleh-pdf/", havaleh, name='havaleh-pdf'),
    path("api/get_last_10_sales/", get_last_10_sales, name='get_last_10_sales'),
    path("api/save_buyer_info/", save_buyer_info, name='save_buyer_info'),
    path("api/get_buyers_list/", get_buyers_list, name='get_buyers_list'),

    # Page routes
    path("", invoice_page, name='invoice_page'),
    path("sales_order/", sales_order, name='sales_order'),
    path("havaleh/", havaleh, name='havaleh'),  # Added trailing slash

    # path('havaleh_pdf/', havale_pdf, name='havaleh_pdf'),
    # path('confirm_sales_invoice/', confirm_sales_invoice, name='confirm_sales_invoice'),
    # path('create_test_sale/', create_test_sale, name='create_test_sale'),
    # path('latest_invoice/', latest_invoice, name='latest_invoice'),
    # path('get_next_sales_invoice/', get_next_sales_invoice, name='get_next_sales_invoice'),
    # path('check_pending_invoice/', check_pending_invoice, name='check_pending_invoice'),

    # path("api/sales-order-pdf/", sales_order, name='sales-order-pdf'),
    # path("test-api/", lambda request: render(request, 'test_api.html')),
    # path("api/latest-invoice/", latest_invoice),
]