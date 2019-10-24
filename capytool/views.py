from django.shortcuts import render
import requests
from .models import Invoice
from .core import invoices as _in
from django.http import HttpResponse

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
    stuff_for_frontend = {'invoice': invoice}
    return render(request, 'capytool/invoice_detail.html', stuff_for_frontend)

def display_pdf(request, idi):
    invoice = Invoice.objects.get(idi=idi)
    pdf = _in.render_to_pdf('capytool/invoice_pdf.html', invoice.__dict__)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %(invoice.__dict__['idi'])
        download = request.GET.get("download")
        content = "inline; filename='%s'"%(filename)
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")