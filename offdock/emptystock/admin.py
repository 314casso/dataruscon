from django.contrib import admin
from emptystock.models import Person, Contact, Sms


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    inlines = (ContactInline,)

class SmsAdmin(admin.ModelAdmin):
    list_display = ('smsid', 'date', 'sender', 'text', 'status', 'http_code')
    search_fields = ['smsid', 'sender', 'text']
    

admin.site.register(Person, PersonAdmin)
admin.site.register(Contact)
admin.site.register(Sms, SmsAdmin)
