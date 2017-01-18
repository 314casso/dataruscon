# -*- coding: utf-8 -*-
from emptystock.models import Sms
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from offdock.local_settings import SMS_SERVICE, WEB_SERVISES
import requests
from emptystock.services import StockDataService
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from datetime import datetime
from lxml import etree
import re


def sendsms(message, target, sms_service_name):
    sms_service = SMS_SERVICE[sms_service_name]
    data = {
               'user': sms_service['USER'],
               'pass': sms_service['PASSWORD'],
               'action': 'post_sms',               
               'message': message,
               'target': target,
               'sender': sms_service['SENDER']               
               }    
    r = requests.post(sms_service['URL'], auth=(sms_service['USER'], sms_service['PASSWORD']), data=data)    
    return r


@receiver(post_save, sender=Sms)
def send_sms_reply(sender, instance, **kwargs):        
    if instance.status == Sms.NEW:        
        dlist = re.findall('\d+', instance.text)        
        first_num = int(dlist[0]) if len(dlist) > 0 else 0 
        stock_data_service = StockDataService(WEB_SERVISES['stockdata'])
        if first_num == SMS_SERVICE['emptystock']['ID']:
            simple_data = stock_data_service.get_simple_data()        
            rendered = render_to_string('sms.txt', {
                                                    'stock_simple_data': simple_data,
                                                    'subtitle' : force_unicode('Прием порожних на РУСКОН {:%d.%m.%Y %H:%M}'.format(datetime.now()))
                                                    })
        elif first_num == 0:
            rendered = u'Ваш SMS запрос "%s" не распознан. Доступные коды:\n1 - Прием порожних' % instance.text
                  
        r = sendsms(rendered, instance.sender, 'emptystock')
        instance.http_code = r.status_code
        instance.xml_response = r.content
        root = etree.fromstring(r.content) 
        errors = root.xpath('//errors/error')
        errors_count = len(errors)       
        if errors_count == 0:
            instance.status = Sms.PROCESSED
        else:            
            instance.status = Sms.ERROR
        instance.save()
        
                 
            