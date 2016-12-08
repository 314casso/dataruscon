# -*- coding: utf-8 -*-
from django.shortcuts import render
from emptystock.services import StockDataService
from offdock.local_settings import WEB_SERVISES, EMAIL_FEEDBACK,\
    DEFAULT_FROM_EMAIL
from django.utils.encoding import force_unicode
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import loader, Context
from django.core.mail import EmailMessage
from django.contrib.sites.models import get_current_site
from django.http import HttpResponse
from emptystock.models import Person



def stockdata(request):    
    stock_data_service = StockDataService(WEB_SERVISES['stockdata'])
    stock_data = stock_data_service.get_data()    
    stock_simple_data = stock_data_service.get_simple_data()
    context = {
               'title' : force_unicode('Терминал Рускон'),
               'subtitle' : force_unicode('Прием порожних контейнеров на {:%d.%m.%Y}'.format(datetime.now())),
               'stock_data' : stock_data,
               'stock_simple_data': stock_simple_data,
              }     
    return render(request, 'stockdata.html', context)


def contacts(request):    
    persons = Person.objects.filter(is_active=True) 
    context = {
               'title' : force_unicode('Контакты'),
               'subtitle' : force_unicode('Контактные лица терминала Рускон'),
               'persons': persons,               
              }     
    return render(request, 'contacts.html', context)


@require_http_methods(["POST"])
@ensure_csrf_cookie
def send_email(request):
    mailto = EMAIL_FEEDBACK    
    t = loader.get_template('email.txt')
    c = Context(request.POST)
    c.update({'site': get_current_site(request)})    
    rendered = t.render(c)
    email = EmailMessage(
        force_unicode('Обращение через сайт'),
        force_unicode(rendered),
        DEFAULT_FROM_EMAIL,
        [mailto]        
    )
    email.send(False)
    return HttpResponse('SUCCESS')    