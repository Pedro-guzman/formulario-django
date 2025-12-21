from django.shortcuts import render, redirect
from .models import Servicios, IngresosDiarios
from .forms import ServiceForm, IngresosDiariosForm
from django.http import HttpResponse
from django.contrib import messages
import plotly.graph_objs as go
import plotly.offline as opy
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from datetime import datetime



def index(request):
    servicios = Servicios.objects.filter(cliente__contains=request.GET.get('search', ''))
    context = {
        'servicios': servicios
    }
    return render(request, 'servicios/index.html', context)

# vista detalles
def view(request, id):
    servicio = Servicios.objects.get(id=id)
    context = {
        'servicio': servicio
    }
    return render(request, 'servicios/detail.html', context)

# Vista para añadir
def edit(request, id):
    servicios = Servicios.objects.get(id=id)
    
    if (request.method == 'GET'):
        form = ServiceForm(instance=servicios)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'servicios/edit.html', context )
    if (request.method == 'POST' ):
        form = ServiceForm(request.POST, instance=servicios)
        form.save()
        
        context = {
            'form': form,
            'id': id
        }
        messages.success(request, "¡Servicio editado exitosamente!")    
        return render(request, 'servicios/edit.html', context)
    
# Crear nuevo servicio
def create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio creado correctamente')
            return redirect('servicios')
    else:
        form = ServiceForm()

    context = {
        'form': form
    }
    return render(request, 'servicios/create.html', context)

# Eliminar servicio
def delete(request, id):
    servicio = Servicios.objects.get(id=id)
    servicio.delete()
    return redirect('servicios')

# Vista para hacer gráfica, servicios realizados
def dashboard(request):
    graficas = []

    # Capturamos fechas del GET
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    servicios = Servicios.objects.all()

    # Si hay fechas, aplicamos el filtro
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d")
            servicios = servicios.filter(fecha__range=(fecha_inicio_obj, fecha_fin_obj))
        except ValueError:
            pass  # Si las fechas son inválidas, no hacemos el filtro

    #  Servicios por tipo
    servicios_data = servicios.values('servicio').annotate(total=Count('id'))
    labels1 = [item['servicio'] for item in servicios_data]
    valores1 = [item['total'] for item in servicios_data]
    trace1 = go.Bar(x=labels1, y=valores1)
    fig1 = go.Figure(data=[trace1], layout=go.Layout(title='Servicios por tipo', yaxis=dict(tickformat='d')))
    graficas.append(opy.plot(fig1, auto_open=False, output_type='div'))

    #  Servicios por día
    servicios_dia = servicios.values('fecha').annotate(total=Count('id')).order_by('fecha')
    labels2 = [str(item['fecha']) for item in servicios_dia]
    valores2 = [item['total'] for item in servicios_dia]
    trace2 = go.Bar(x=labels2, y=valores2)
    fig2 = go.Figure(data=[trace2], layout=go.Layout(title='Servicios por día', yaxis=dict(tickformat='d')))
    graficas.append(opy.plot(fig2, auto_open=False, output_type='div'))

    #  Porcentaje por peluquero
    servicios_peluquero = servicios.values('barbero').annotate(total=Count('id'))
    labels3 = [item['barbero'] for item in servicios_peluquero]
    valores3 = [item['total'] for item in servicios_peluquero]
    trace3 = go.Pie(labels=labels3, values=valores3)
    fig3 = go.Figure(data=[trace3], layout=go.Layout(title='Servicios por peluquero'))
    graficas.append(opy.plot(fig3, auto_open=False, output_type='div'))

    #  Porcentaje por método de pago
    pagos = servicios.values('metodo_pago').annotate(total=Count('id'))
    labels4 = [item['metodo_pago'] for item in pagos]
    valores4 = [item['total'] for item in pagos]
    trace4 = go.Pie(labels=labels4, values=valores4)
    fig4 = go.Figure(data=[trace4], layout=go.Layout(title='Métodos de pago'))
    graficas.append(opy.plot(fig4, auto_open=False, output_type='div'))

    return render(request, 'servicios/dashboard.html', {
        'graficas': graficas
    })


# Nueva vista para registrar ingresos diarios
def registrar_ingresos(request):
    if request.method == 'POST':
        form = IngresosDiariosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingresos registrados correctamente')
            return redirect('registrar_ingresos')
    else:
        form = IngresosDiariosForm()
    
    # Mostrar los últimos ingresos registrados
    ingresos = IngresosDiarios.objects.all().order_by('-fecha')[:10]
    
    return render(request, 'servicios/registrar_ingresos.html', {
        'form': form,
        'ingresos': ingresos
    })

# Vista para listar todos los ingresos
def lista_ingresos(request):
    ingresos = IngresosDiarios.objects.all().order_by('-fecha')
    
    # Calcular totales generales
    totales = ingresos.aggregate(
        total_efectivo=Sum('efectivo'),
        total_tarjeta=Sum('tarjeta'),
        total_transferencia=Sum('transferencia')
    )
    
    # Calcular el gran total
    gran_total = (totales['total_efectivo'] or 0) + (totales['total_tarjeta'] or 0) + (totales['total_transferencia'] or 0)
    
    context = {
        'ingresos': ingresos,
        'totales': totales,
        'gran_total': gran_total
    }
    return render(request, 'servicios/lista_ingresos.html', context)

# Vista para editar ingresos
def editar_ingreso(request, id):
    ingreso = IngresosDiarios.objects.get(id=id)
    
    if request.method == 'GET':
        form = IngresosDiariosForm(instance=ingreso)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'servicios/editar_ingreso.html', context)
    
    if request.method == 'POST':
        form = IngresosDiariosForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Ingreso editado exitosamente!")
            return redirect('lista_ingresos')
        
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'servicios/editar_ingreso.html', context)

# Vista para eliminar ingresos
def eliminar_ingreso(request, id):
    ingreso = IngresosDiarios.objects.get(id=id)
    ingreso.delete()
    messages.success(request, 'Ingreso eliminado correctamente')
    return redirect('lista_ingresos')