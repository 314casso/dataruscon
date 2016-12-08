from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from emptystock.views import stockdata, send_email, contacts
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'offdock.views.home', name='home'),
    # url(r'^offdock/', include('offdock.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', 
    url(r'^$', stockdata, name='stockdata'), 
    url(r'^sendmail/$', send_email, name='sendmail'),
    url(r'^contacts/$', contacts, name='contacts'),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns