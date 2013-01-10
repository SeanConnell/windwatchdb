from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'icarus.views.index', name='home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^site/([0-9]+)', 'icarus.views.site'),
    #List of sites if the user wants to look at a specific one for some reason
    url(r'^site/list', 'icarus.views.site_list'),
    url(r'^about', 'icarus.views.about'),
    url(r'^day/([0-9]+)', 'icarus.views.day'),
)
