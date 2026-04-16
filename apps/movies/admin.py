from django.contrib import admin
from .models import Bloque, Unidad, Pago, Reserva


@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'numero_pisos', 'created')


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bloque', 'propietario', 'created')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('name', 'unidad', 'monto', 'fecha_pago', 'estado')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('name', 'unidad', 'amenidad', 'fecha_reserva')
