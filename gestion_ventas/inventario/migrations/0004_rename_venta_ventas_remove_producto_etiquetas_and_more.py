# Generated by Django 5.1 on 2024-10-04 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_etiqueta_rename_stock_producto_cantidad_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Venta',
            new_name='Ventas',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='etiquetas',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]