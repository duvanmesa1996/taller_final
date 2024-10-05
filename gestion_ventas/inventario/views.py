from django.views.decorators.http import require_POST
import csv
import io
from io import BytesIO
import tempfile
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Producto, Categoria, Proveedor, DetalleProducto, Ventas, Cliente
from .forms import ProductoForm, CategoriaForm, ProveedorForm, ClienteForm, VentasForm
#DetalleProductoForm


# Create your views here.
@require_POST
def eliminar_ventas(request):
    venta_ids = request.POST.getlist('venta_ids')
    if venta_ids:
        Ventas.objects.filter(id__in=venta_ids).delete()
    return redirect('lista_ventas') 

def inicio(request):
    return render(request, 'inicio.html')

def assign_user_group(sender, request, user, **kwargs):
    group = Group.object.get(name='Usuarios Regulares')
    user.groups.add(group)

def my_view(request):
    if not request.user.has_perm('inventario.view_producto'):
        return redirect('no-access')

def listar_productos(request):
    productos = Producto.objects.prefetch_related('detalleproducto').all()
    return render(request, 'listar_productos.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        if producto_form.is_valid():
            producto_form.save()
            return redirect('listar_productos')
    else:
        producto_form = ProductoForm()

    return render(request, 'agregar_producto.html', {'producto_form': producto_form})

from django.shortcuts import get_object_or_404

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'detalle_producto.html', {'producto': producto})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    try:
        detalle = producto.detalleproducto
    except DetalleProducto.DoesNotExist:
        detalle = None

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, instance=producto)
        
        if producto_form.is_valid(): 
            producto = producto_form.save(commit=False)
            producto_form.save()
            producto_form.save_m2m()           
            return redirect('listar_productos')
    else:
        producto_form = ProductoForm(instance=producto)
     
    return render(request, 'editar_producto.html', {
        'producto_form': producto_form,
        
    })

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})


def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})

def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form})

def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('listar_proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})

def listar_ventas(request):
    ventas = Ventas.objects.all().select_related('producto', 'cliente')
    return render(request, 'listar_ventas.html', {'ventas': ventas})

def registrar_venta(request):
    if request.method == 'POST':
        form = VentasForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto

            
            if producto.cantidad >= venta.cantidad:
                venta.total = producto.precio * venta.cantidad
                producto.cantidad -= venta.cantidad
                producto.save()
                venta.save()  
                return redirect('listar_ventas')
            else:
                form.add_error('cantidad', 'No hay suficiente stock para realizar esta venta.')
    else:
        form = VentasForm()

    return render(request, 'registrar_ventas.html', {'form': form})

def editar_venta(request, id):
    venta = get_object_or_404(Ventas, id=id)
    
    if request.method == 'POST':
        form = VentasForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('listar_ventas') 
    else:
        form = VentasForm(instance=venta)
    
    return render(request, 'editar_ventas.html', {'form': form, 'venta': venta})


def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'agregar_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

