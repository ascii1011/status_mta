from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'mta.views.home', name='home'),
    url(r'^about/$', 'mta.views.about', name='about'),

    url(r'^service/status/$', 'mta.views.get_service_status', name='service-status'),

    url(r'^favorites/$', 'mta.views.get_favorites', name='get-favorites'),
    url(r'^favorite/remove/$', 'mta.views.remove_favorite', name='remove-favorite'),
    url(r'^favorite/add/$', 'mta.views.add_favorite', name='addd-favorite'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
