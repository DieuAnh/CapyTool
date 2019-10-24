from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('invoices/', views.show_invoices, name='invoices'),
    path('invoices/<str:idi>', views.show_detail, name='invoice_detail'),
    path('invoices/<str:idi>/pdf', views.display_pdf, name='invoice_pdf')
]