# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
import random
register = template.Library()

@register.filter()
def hide_email(email, protocol):    
    name = email
    mailto_link = u'<a href="%s:%s">%s</a>' % (protocol, encode_string(email), encode_string(name))

    value = '<script type="text/javascript">// <![CDATA['+"\n \
           \tdocument.write('%s')\n \
           \t// ]]></script>\n" % (mailto_link)
    return mark_safe(value.strip())

def encode_string(value):
    """
    Encode a string into it's equivalent html entity.
    
    The tag will randomly choose to represent the character as a hex digit or
    decimal digit.
    """    
    e_string = "" 
    for a in value:
        t = random.randint(0,1)
        if t:
            en = "&#x%x;" % ord(a)
        else:
            en = "&#%d;" % ord(a)
        e_string += en 
    return e_string