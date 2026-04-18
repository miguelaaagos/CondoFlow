from django.urls import re_path, include
from apps.movies import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'movies'

pago_patterns = [
    re_path(r'^$', views.pago_list, name='pago-list'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.pago_detail, name='pago-detail'),
    re_path(r'^crear/$', views.pago_create, name='pago-create'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.pago_update, name='pago-edit'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.pago_delete, name='pago-delete'),
]

reserva_patterns = [
    re_path(r'^$', views.reserva_list, name='reserva-list'),
    re_path(r'^crear/$', views.reserva_create, name='reserva-create'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.reserva_delete, name='reserva-delete'),
]

unidad_patterns = [
    re_path(r'^$', views.unidad_list, name='unidad-list'),
    re_path(r'^crear/$', views.unidad_create, name='unidad-create'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.unidad_update, name='unidad-edit'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.unidad_delete, name='unidad-delete'),
]

bloque_patterns = [
    re_path(r'^$', views.bloque_list, name='bloque-list'),
    re_path(r'^crear/$', views.bloque_create, name='bloque-create'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.bloque_update, name='bloque-edit'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.bloque_delete, name='bloque-delete'),
]

anuncio_patterns = [
    re_path(r'^$', views.anuncio_list, name='anuncio-list'),
    re_path(r'^crear/$', views.anuncio_create, name='anuncio-create'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.anuncio_update, name='anuncio-edit'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.anuncio_delete, name='anuncio-delete'),
]

urlpatterns = [
    re_path(r'^$', views.log_in, name='log-in'),
    re_path(r'^log-out/$', views.log_out, name='log-out'),
    re_path(r'^inicio/$', views.home, name='home'),
    re_path(r'^pagos/', include(pago_patterns)),
    re_path(r'^reservas/', include(reserva_patterns)),
    re_path(r'^unidades/', include(unidad_patterns)),
    re_path(r'^bloques/', include(bloque_patterns)),
    re_path(r'^anuncios/', include(anuncio_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
