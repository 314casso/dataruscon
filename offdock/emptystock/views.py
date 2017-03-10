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
from emptystock.models import Person, Sms
from emptystock.forms import SmsForm
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import logging


logger = logging.getLogger('django.request')


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


def authenticate_user(uname, passwd, request):
    user = authenticate(username=uname, password=passwd)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.user = user

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
                authenticate_user(uname, passwd, request)
    elif 'LOGIN' in request.POST:                
        login = request.POST['LOGIN']
        if login == SMS_SERVICE['emptystock']['USER']:
            authenticate_user(login, SMS_SERVICE['emptystock']['PASSWORD'], request)
    
    if not request.user.is_authenticated():        
        logger.error(request.META)
        logger.error(request.POST)
        return HttpResponse(request.META, status=401)     
    try:       
        Sms.objects.create(agtid=request.POST.get('CNRID', None), 
                          sender=request.POST.get('SENDER', None), 
                          text=request.POST.get('TEXT', None), 
                          smsid=request.POST.get('ORDID', None), 
                          inbox=request.POST.get('SIBNUM', None), 
                          rescount=request.POST.get('RESCOUNT', None), 
                          target=request.POST.get('TARGET', None)
                          )
        return HttpResponse('Accepted', status=202)
    except Exception as e:
        logger.error(request.META)
        logger.error(request.POST)
        logger.error(e.message)
        return HttpResponse(e.message, status=422)    
    
    return HttpResponse('Bad Request', status=400)    