import requests
from lxml import etree
from django.utils.encoding import force_unicode

r = requests.post('http://127.0.0.1:8000/sms/', auth=('ruscon', 'V5FnWzUdXj'), data={'ordid':98, 'sender':'+79615892001', 'target': '+79615892001', })
print r.status_code
print r.text


# r = requests.post('http://beeline.amega-inform.ru/sendsms/', auth=('KRD_RUSCON1', '9054956328'), data={
#                                                                                                 'action':'status', 
#                                                                                                 'sms_id':'725209660', 
#                                                                                                 'user': 'KRD_RUSCON1', 
#                                                                                                 'pass': '9054956328'
#                                                                                                 })
#  
# print r.status_code
# 
# if r.status_code == 200:
#     print "OK" 

# 
# root = etree.fromstring(r.content)
# print etree.tostring(root, pretty_print=True, encoding='UTF-8')
# rsl = root.xpath('//SMS_TEXT/text()')
# print rsl[0]