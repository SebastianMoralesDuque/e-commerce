# Generated by Django 4.2.1 on 2023-06-20 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='venta',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='resena',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='resena',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='metodo_pago',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='producto',
        ),
        migrations.DeleteModel(
            name='Carrito',
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.DeleteModel(
            name='Factura',
        ),
        migrations.DeleteModel(
            name='MetodoPago',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
        migrations.DeleteModel(
            name='Resena',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Venta',
        ),
    ]
