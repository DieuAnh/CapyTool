from django.shortcuts import render
import requests
from .models import Invoice
from .core import invoices as _in

# Create your views here.
def login(request):
    return render(request, 'capytool/login.html')

def show_invoices(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    res = _in.scrape_invoice(email, password)
    invoices = res['invoices']
    if res['success']:
        for invoice in invoices:
            if not Invoice.objects.filter(idi=invoice['idi']).exists():
                new_inv = _in.add_invoice_todb(invoice)
        stuff_for_frontend = {'invoices': res['invoices'], 'message': res['message']}
        return render(request, 'capytool/invoices.html', stuff_for_frontend)
    else:
        return render(request, 'capytool/login.html')

def show_detail(request, idi):
    invoice = Invoice.objects.get(idi=idi)
    print('invoice returned is ', invoice, type(invoice))
    stuff_for_frontend = {'invoice': invoice}
    return render(request, 'capytool/invoice_detail.html', stuff_for_frontend)