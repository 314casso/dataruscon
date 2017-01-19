# -*- coding: utf-8 -*-
from django.db import models
import os
from django.utils.encoding import force_unicode 
import datetime

def get_upload_path(instance, filename):
    return os.path.join(
      "persons", filename)

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50 , null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    foto = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.first_name

class Contact(models.Model):
    EMAIL = 1
    PHONE = 2
    FAX = 3
    TYPE_CHOICES = (
        (EMAIL, 'Email'),
        (PHONE, force_unicode('Тел')),
        (FAX, force_unicode('Факс')),        
    )
    contact = models.CharField(max_length=50)    
    type = models.IntegerField(choices=TYPE_CHOICES, default=PHONE)
    person = models.ForeignKey(Person)
    
    def type_protocol(self):
        mapper = {
                  self.EMAIL: 'mailto',
                  self.PHONE: 'tel',
                  self.FAX: 'tel',
                  }
        if self.type in mapper:
            return mapper.get(self.type)
        
    class Meta:        
        unique_together = ("contact", "type")
    def __unicode__(self):
        return u'{0} {1}'.format(self.get_type_display(), self.contact) 


class Sms(models.Model):
    NEW = 1
    PROCESSED = 2
    ERROR = 3
    
    STATUS_CHOICES = (
        (NEW, force_unicode('Новое')),
        (PROCESSED, force_unicode('Обработано')),
        (ERROR, force_unicode('Обшибка')),        
    )
      
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)     
    smsid = models.CharField('SMS ID', max_length=50, db_index=True, unique=True) 
    agtid = models.CharField('AGT ID', max_length=50, null=True, blank=True) 
    inbox = models.CharField('ID входящего ящика', max_length=255, null=True, blank=True) 
    sender = models.CharField('Номер отправителя', max_length=255)
    target = models.CharField('Номер получателя', max_length=255)
    rescount = models.CharField('Количество для тарификации', max_length=50, null=True, blank=True) 
    text = models.TextField('Текст сообщения', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW, db_index=True, blank=True)
    http_code = models.CharField('HTTP Код', max_length=50, null=True, blank=True)
    xml_response = models.TextField('XML ответ', null=True, blank=True)  
    
    def __unicode__(self):
        return u'{0}'.format(self.smsid)  

import signals    # @UnusedImport