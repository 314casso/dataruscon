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


def send_sms(message, target):
    beeline = SMS_SERVICE['beeline']
    data = {
               'user': beeline['USER'],
               'pass': beeline['PASSWORD'],
               'action': 'post_sms',               
               'message': message,
               'target': target               
               }    
    r = requests.post(beeline['URL'], auth=(beeline['USER'], beeline['PASSWORD']), data=data)    
    return r


@receiver(post_save, sender=Sms)
def send_sms_reply(sender, instance, **kwargs):    
    if instance.status == Sms.NEW:
        stock_data_service = StockDataService(WEB_SERVISES['stockdata'])
        simple_data = stock_data_service.get_simple_data()        
        rendered = render_to_string('sms.txt', {
                                                'stock_simple_data': simple_data,
                                                'subtitle' : force_unicode('Прием порожних на РУСКОН {:%d.%m.%Y %H:%M}'.format(datetime.now()))
                                                })      
        r = send_sms(rendered, instance.sender)
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
            