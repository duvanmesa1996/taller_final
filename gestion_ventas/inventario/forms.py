from django import forms
from .models import Producto, Categoria, Proveedor, DetalleProducto, Cliente
from .models import Ventas
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'proveedor', 'cantidad', 'precio', 'descripcion']
       

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError('El nombre no puede quedar vacio.')
        if len(nombre) <= 3:
            raise forms.ValidationError('el nombre debe tener al menos 3 caracteres.')
        return nombre

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('el numero de telefono debe contener solo digitos.')
        return telefono

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'direccion']


class VentasForm(forms.ModelForm):
   
    class Meta:
        model = Ventas
        fields = ['producto', 'cliente', 'cantidad']
