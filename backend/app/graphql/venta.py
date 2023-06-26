import graphene
from graphene_django import DjangoObjectType
from ..models import Venta

class VentaType(DjangoObjectType):
    class Meta:
        model = Venta

class VentaQuery(graphene.ObjectType):
    ventas = graphene.List(VentaType)

    def resolve_ventas(self, info):
        return Venta.objects.all()

class CrearVentaMutation(graphene.Mutation):
    class Arguments:
        usuario_id = graphene.ID(required=True)
        carrito_id = graphene.ID(required=True)
        metodo_pago_id = graphene.ID(required=True)
        precio_total = graphene.Decimal(required=True)

    venta = graphene.Field(VentaType)

    def mutate(self, info, usuario_id, carrito_id, metodo_pago_id, precio_total):
        venta = Venta.objects.create(
            usuario_id=usuario_id,
            carrito_id=carrito_id,
            metodo_pago_id=metodo_pago_id,
            precio_total=precio_total
        )

        return CrearVentaMutation(venta=venta)

class EditarVentaMutation(graphene.Mutation):
    class Arguments:
        venta_id = graphene.ID(required=True)
        usuario_id = graphene.ID()
        carrito_id = graphene.ID()
        metodo_pago_id = graphene.ID()
        precio_total = graphene.Decimal()

    venta = graphene.Field(VentaType)

    def mutate(self, info, venta_id, usuario_id=None, carrito_id=None, metodo_pago_id=None, precio_total=None):
        venta = Venta.objects.get(pk=venta_id)

        if usuario_id is not None:
            venta.usuario_id = usuario_id
        if carrito_id is not None:
            venta.carrito_id = carrito_id
        if metodo_pago_id is not None:
            venta.metodo_pago_id = metodo_pago_id
        if precio_total is not None:
            venta.precio_total = precio_total

        venta.save()

        return EditarVentaMutation(venta=venta)

class EliminarVentaMutation(graphene.Mutation):
    class Arguments:
        venta_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, venta_id):
        try:
            Venta.objects.get(pk=venta_id).delete()
            success = True
        except Venta.DoesNotExist:
            success = False

        return EliminarVentaMutation(success=success)

class VentaMutation(graphene.ObjectType):
    crear_venta = CrearVentaMutation.Field()
    editar_venta = EditarVentaMutation.Field()
    eliminar_venta = EliminarVentaMutation.Field()

