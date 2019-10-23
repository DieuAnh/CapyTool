import requests
import urllib.parse
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
from ..models import Invoice
from datetime import datetime

def get_content(className):
    return (item.find(class_=className).get_text()).strip()

def get_float_from_string(string):
    return float(string.replace(u'\xa0', u'').replace(',', '.').replace('€', ''))

def scrape_invoice(email, password):
    with requests.Session() as s:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'app.factomos.com',
            'Sec-Fetch-User': '?1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Referer': 'https://app.factomos.com/dashboard',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'
        }
        s.headers.update(headers)
        data = {
            'url': 'https://app.factomos.com/connexion',
            'appAction': 'login',
            'email': email,
            'password': password,
        }
        resPost = s.post('https://app.factomos.com//controllers/app-pro/login-ajax.php', headers=headers, data=data, allow_redirects=True)
        statusCode = resPost.status_code
        invoices = []
        if statusCode == requests.codes.ok:
            res = s.get('https://app.factomos.com/mes-factures?&subFilter=valid')
            soup = bs(res.text, 'html.parser')
            items = soup.find_all(class_='item-bg')
            for item in items:
                invoice = {}
                invoice['idi'] = get_content('ITEM-NUMBER')
                date_str = get_content('ITEM-DATE')
                invoice['created_at'] = datetime.strptime(date_str, "%d/%m/%y").date()
                invoice['client_name'] = get_content('ITEM-CLIENT')
                total_ttc_str = get_content('ITEM-TOT-TTC')
                invoice['total_ttc'] = get_float_from_string(total_ttc_str)
                total_tva_str = get_content('ITEM-TOT-TVA')
                invoice['total_tva'] = get_float_from_string(total_tva_str)
                invoice['email'] = email
                invoices.append(invoice)
            return {'success': True, 'message': 'Login succeeded', 'invoices': invoices}
        return {'success': status_code, 'message': 'Login failed', 'invoices': invoices}

def add_invoice_todb(invoice):
    if invoice: 
        inv = Invoice(idi=invoice['idi'], created_at=invoice['created_at'], client_name=invoice['client_name'], total_ttc=invoice['total_ttc'], total_tva=invoice['total_tva'], email=invoice['email'])
        inv.save()
        return True
    return False
