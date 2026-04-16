from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import PagoForm, ReservaForm, UnidadForm, BloqueForm, AnuncioForm, LoginForm
from .models import Pago, Reserva, Unidad, Bloque, Anuncio


# Solo permite acceso a administradores (is_staff)
def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'No tienes permiso para acceder a esta seccion.')
            return redirect('movies:home')
        return view_func(request, *args, **kwargs)
    return wrapper


# Login / Logout

def log_in(request):
    form = LoginForm(request.POST or None)
    context = {'message': None, 'form': form}
    if request.POST and form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('movies:home')
            else:
                context['message'] = 'El usuario ha sido desactivado'
        else:
            context['message'] = 'Usuario o contrasena incorrecta'
    return render(request, 'movies/login.html', context)


@login_required
def log_out(request):
    logout(request)
    return redirect('movies:log-in')


# Inicio / Dashboard

@login_required
def home(request):
    hoy = date.today()
    anuncios = Anuncio.objects.order_by('-destacado', '-created')[:4]

    if request.user.is_staff:
        pagos_mes = Pago.objects.filter(
            fecha_pago__month=hoy.month,
            fecha_pago__year=hoy.year
        )
        total_recaudado = pagos_mes.filter(estado='pagado').aggregate(
            total=Sum('monto')
        )['total'] or 0

        context = {
            'es_admin': True,
            'total_recaudado': total_recaudado,
            'pagos_pendientes': Pago.objects.filter(estado='pendiente').count(),
            'pagos_vencidos': Pago.objects.filter(estado='vencido').count(),
            'total_unidades': Unidad.objects.count(),
            'proximas_reservas': Reserva.objects.filter(
                fecha_reserva__gte=hoy
            ).order_by('fecha_reserva')[:5],
            'ultimos_pagos': Pago.objects.select_related('unidad')[:5],
            'anuncios': anuncios,
        }
    else:
        try:
            unidad = request.user.unidad
            mis_pagos = Pago.objects.filter(unidad=unidad).order_by('-fecha_pago')
            pago_mes = mis_pagos.filter(
                fecha_pago__month=hoy.month,
                fecha_pago__year=hoy.year
            ).first()
            context = {
                'es_admin': False,
                'unidad': unidad,
                'pago_mes': pago_mes,
                'mis_pagos': mis_pagos[:5],
                'mis_reservas': Reserva.objects.filter(
                    unidad=unidad, fecha_reserva__gte=hoy
                ).order_by('fecha_reserva')[:3],
                'anuncios': anuncios,
            }
        except Unidad.DoesNotExist:
            context = {'es_admin': False, 'anuncios': anuncios}

    return render(request, 'movies/home.html', context)


# Pagos

@login_required
def pago_list(request):
    if request.user.is_staff:
        pagos = Pago.objects.select_related('unidad', 'unidad__bloque').all()
    else:
        try:
            pagos = Pago.objects.filter(unidad=request.user.unidad)
        except Unidad.DoesNotExist:
            pagos = Pago.objects.none()

    estado = request.GET.get('estado')
    if estado in ['pendiente', 'pagado', 'vencido']:
        pagos = pagos.filter(estado=estado)

    return render(request, 'movies/index.html', {
        'pagos': pagos,
        'estado_filtro': estado,
    })


@login_required
def pago_detail(request, pk):
    try:
        pago = Pago.objects.get(pk=pk)
    except Pago.DoesNotExist:
        raise Http404('Este pago no existe')
    if not request.user.is_staff:
        try:
            if pago.unidad != request.user.unidad:
                return redirect('movies:home')
        except Unidad.DoesNotExist:
            return redirect('movies:home')
    return render(request, 'movies/detail.html', {'pago': pago})


@admin_required
def pago_create(request, **kwargs):
    form = PagoForm(request.POST or None, request.FILES or None)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Pago registrado correctamente.')
        return redirect('movies:pago-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Registrar Pago'})


@admin_required
def pago_update(request, **kwargs):
    pago = Pago.objects.get(pk=kwargs.get('pk'))
    form = PagoForm(request.POST or None, request.FILES or None, instance=pago)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Pago actualizado correctamente.')
        return redirect('movies:pago-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Editar Pago'})


@admin_required
def pago_delete(request, **kwargs):
    pago = Pago.objects.get(pk=kwargs.get('pk'))
    if request.POST:
        pago.delete()
        messages.success(request, 'Pago eliminado.')
        return redirect('movies:pago-list')
    return render(request, 'movies/confirm_delete.html', {
        'objeto': pago, 'tipo': 'el pago'
    })


# Reservas

@login_required
def reserva_list(request):
    if request.user.is_staff:
        reservas = Reserva.objects.select_related('unidad').all()
    else:
        try:
            reservas = Reserva.objects.filter(unidad=request.user.unidad)
        except Unidad.DoesNotExist:
            reservas = Reserva.objects.none()
    return render(request, 'movies/reserva/reserva_list.html', {'reservas': reservas})


@login_required
def reserva_create(request, **kwargs):
    form = ReservaForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Reserva creada correctamente.')
        return redirect('movies:reserva-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Nueva Reserva'})


@login_required
def reserva_delete(request, **kwargs):
    reserva = Reserva.objects.get(pk=kwargs.get('pk'))
    if request.POST:
        reserva.delete()
        messages.success(request, 'Reserva eliminada.')
        return redirect('movies:reserva-list')
    return render(request, 'movies/confirm_delete.html', {
        'objeto': reserva, 'tipo': 'la reserva'
    })


# Unidades

@login_required
def unidad_list(request):
    unidades = Unidad.objects.select_related('bloque').all()
    return render(request, 'movies/unidad/unidad_list.html', {'unidades': unidades})


@admin_required
def unidad_create(request, **kwargs):
    form = UnidadForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Unidad creada correctamente.')
        return redirect('movies:unidad-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Nueva Unidad'})


@admin_required
def unidad_update(request, **kwargs):
    unidad = Unidad.objects.get(pk=kwargs.get('pk'))
    form = UnidadForm(request.POST or None, instance=unidad)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Unidad actualizada correctamente.')
        return redirect('movies:unidad-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Editar Unidad'})


@admin_required
def unidad_delete(request, **kwargs):
    unidad = Unidad.objects.get(pk=kwargs.get('pk'))
    if request.POST:
        unidad.delete()
        messages.success(request, 'Unidad eliminada.')
        return redirect('movies:unidad-list')
    return render(request, 'movies/confirm_delete.html', {
        'objeto': unidad, 'tipo': 'la unidad'
    })


# Anuncios

@login_required
def anuncio_list(request):
    anuncios = Anuncio.objects.all()
    return render(request, 'movies/anuncio/anuncio_list.html', {'anuncios': anuncios})


@admin_required
def anuncio_create(request, **kwargs):
    form = AnuncioForm(request.POST or None)
    if request.POST and form.is_valid():
        anuncio = form.save(commit=False)
        anuncio.autor = request.user
        anuncio.save()
        messages.success(request, 'Anuncio publicado correctamente.')
        return redirect('movies:anuncio-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Nuevo Anuncio'})


@admin_required
def anuncio_update(request, **kwargs):
    anuncio = Anuncio.objects.get(pk=kwargs.get('pk'))
    form = AnuncioForm(request.POST or None, instance=anuncio)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Anuncio actualizado.')
        return redirect('movies:anuncio-list')
    return render(request, 'movies/form.html', {'form': form, 'titulo': 'Editar Anuncio'})


@admin_required
def anuncio_delete(request, **kwargs):
    anuncio = Anuncio.objects.get(pk=kwargs.get('pk'))
    if request.POST:
        anuncio.delete()
        messages.success(request, 'Anuncio eliminado.')
        return redirect('movies:anuncio-list')
    return render(request, 'movies/confirm_delete.html', {
        'objeto': anuncio, 'tipo': 'el anuncio'
    })
