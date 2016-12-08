# -*- coding: utf-8 -*-
from django.db import models
import os
from django.utils.encoding import force_unicode

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
    class Meta:        
        unique_together = ("contact", "type")
    def __unicode__(self):
        return u'{0} {1}'.format(self.get_type_display(), self.contact) 
        
    
