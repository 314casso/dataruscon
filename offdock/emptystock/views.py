# -*- coding: utf-8 -*-
from django.shortcuts import render
from emptystock.services import StockDataService
from offdock.local_settings import WEB_SERVISES, EMAIL_FEEDBACK,\
    DEFAULT_FROM_EMAIL, SMS_SERVICE
from django.utils.encoding import force_unicode
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from django.core.mail import EmailMessage
from django.contrib.sites.models import get_current_site
from emptystock.models import Person
from emptystock.forms import SmsForm
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def stockdata(request):    
    stock_data_service = StockDataService(WEB_SERVISES['stockdata'])
    stock_data = stock_data_service.get_data()    
    stock_simple_data = stock_data_service.get_simple_data()
    context = {
               'title' : force_unicode('Терминал Рускон'),
               'subtitle' : force_unicode('Прием порожних контейнеров на {:%d.%m.%Y %H:%M}'.format(datetime.now())),
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
@csrf_exempt
def send_email(request):        
    t = loader.get_template('email.txt')
    c = Context(request.POST)
    c.update({'site': get_current_site(request)})    
    rendered = t.render(c)
    email = EmailMessage(
        force_unicode('Обращение через сайт'),
        force_unicode(rendered),
        DEFAULT_FROM_EMAIL,
        EMAIL_FEEDBACK        
    )
    email.send(False)
    return HttpResponse('SUCCESS')


@csrf_exempt
@require_http_methods(["POST"])
def get_sms(request):  
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
    
    if not request.user.is_authenticated():
        return HttpResponse('Unauthorized', status=401)       
      
    form = SmsForm(request.POST)    
    if form.is_valid():
        form.save()     
        return HttpResponse('Accepted', status=202)
    else:
        return HttpResponse(u'\n'.join([u'\n'.join(errors) for field, errors in form.errors.items()]), status=422)  # @UnusedVariable
    return HttpResponse('Bad Request', status=400)
 
    
    