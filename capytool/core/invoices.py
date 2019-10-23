import requests
import urllib.parse
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
from ..models import Invoice
from datetime import datetime

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
        res_post = s.post('https://app.factomos.com//controllers/app-pro/login-ajax.php', headers=headers, data=data, allow_redirects=True)
        status_code = res_post.status_code
        invoices = []
        if status_code == requests.codes.ok:
            res = s.get('https://app.factomos.com/mes-factures?&subFilter=valid')
            soup = bs(res.text, 'html.parser')
            items = soup.find_all(class_='item-bg')
            for item in items:
                invoice = {}
                invoice['idi'] = (item.find(class_='ITEM-NUMBER').get_text()).strip()
                date_str = (item.find(class_='ITEM-DATE').get_text()).strip()
                invoice['created_at'] = datetime.strptime(date_str, "%d/%m/%y").date()
                invoice['client_name'] = (item.find(class_='ITEM-CLIENT').get_text()).strip()
                total_ttc_str = (item.find(class_='ITEM-TOT-TTC').get_text()).strip()
                invoice['total_ttc'] = float(total_ttc_str.replace(u'\xa0', u'').replace(',', '.').replace('€', ''))
                total_tva_str = (item.find(class_='ITEM-TOT-TVA').get_text()).strip()
                invoice['total_tva'] = float(total_tva_str.replace(u'\xa0', u'').replace(',', '.').replace('€', ''))
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
