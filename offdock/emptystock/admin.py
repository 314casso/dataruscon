from django.contrib import admin
from emptystock.models import Person, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    inlines = (ContactInline,)

admin.site.register(Person, PersonAdmin)
admin.site.register(Contact)
