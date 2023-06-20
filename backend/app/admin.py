from django.contrib import admin
from .models import User, Ciudad, Categoria, Producto, Carrito, ItemCarrito, MetodoPago, Resena, Venta, Factura

admin.site.register(User)
admin.site.register(Ciudad)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MetodoPago)
admin.site.register(Resena)


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 1


class CarritoAdmin(admin.ModelAdmin):
    inlines = (ItemCarritoInline,)


admin.site.register(Carrito, CarritoAdmin)


class VentaAdmin(admin.ModelAdmin):
    model = Venta
    list_display = ('id', 'usuario', 'metodo_pago', 'precio_total')
    list_filter = ('usuario', 'metodo_pago')


admin.site.register(Venta, VentaAdmin)


class FacturaAdmin(admin.ModelAdmin):
    model = Factura
    list_display = ('id', 'venta', 'fecha')
    list_filter = ('venta', 'fecha')


admin.site.register(Factura, FacturaAdmin)
