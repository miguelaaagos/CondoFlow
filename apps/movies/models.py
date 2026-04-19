from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class BaseName(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Bloque(BaseName):
    numero_pisos = models.IntegerField(verbose_name='Numero de pisos')

    class Meta:
        verbose_name = 'Bloque'
        verbose_name_plural = 'Bloques'


class Unidad(BaseName):
    numero = models.CharField(max_length=10, verbose_name='Numero de unidad')
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, verbose_name='Bloque')
    propietario = models.CharField(max_length=150, verbose_name='Propietario')
    usuario = models.OneToOneField(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Usuario residente',
        related_name='unidad'
    )

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['bloque', 'numero']

    def __str__(self):
        return '{} - Depto {} ({})'.format(self.bloque, self.numero, self.propietario)

    def get_edit_url(self):
        return reverse_lazy('movies:unidad-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('movies:unidad-delete', kwargs={'pk': self.pk})


class Pago(BaseName):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ]
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, verbose_name='Unidad')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    fecha_pago = models.DateField(verbose_name='Fecha de pago')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    comprobante = models.ImageField(upload_to='comprobantes', blank=True, null=True, verbose_name='Comprobante')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def get_edit_url(self):
        return reverse_lazy('movies:pago-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('movies:pago-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('movies:pago-detail', kwargs={'pk': self.pk})


class Reserva(BaseName):
    AMENIDADES = [
        ('salon', 'Salon comunal'),
        ('piscina', 'Piscina'),
        ('gym', 'Gimnasio'),
        ('bbq', 'BBQ / Asadores'),
    ]
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, verbose_name='Unidad')
    amenidad = models.CharField(max_length=50, choices=AMENIDADES, verbose_name='Area comun')
    fecha_reserva = models.DateField(verbose_name='Fecha de reserva')
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['fecha_reserva']

    def get_edit_url(self):
        return reverse_lazy('movies:reserva-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('movies:reserva-delete', kwargs={'pk': self.pk})


class Anuncio(BaseName):
    contenido = models.TextField(verbose_name='Contenido')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    destacado = models.BooleanField(default=False, verbose_name='Destacado')

    class Meta:
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'
        ordering = ['-created']

    def get_edit_url(self):
        return reverse_lazy('movies:anuncio-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('movies:anuncio-delete', kwargs={'pk': self.pk})
