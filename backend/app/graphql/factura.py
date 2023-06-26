import graphene
from graphene_django import DjangoObjectType
from ..models import Factura,Venta

class FacturaType(DjangoObjectType):
    class Meta:
        model = Factura

class FacturaQuery(graphene.ObjectType):
    facturas = graphene.List(FacturaType)

    def resolve_facturas(self, info):
        return Factura.objects.all()

class CrearFacturaMutation(graphene.Mutation):
    class Arguments:
        venta_id = graphene.ID(required=True)

    factura = graphene.Field(FacturaType)

    def mutate(self, info, venta_id):
        # Obtener la venta a partir del ID
        venta = Venta.objects.get(id=venta_id)

        # Crear la factura
        factura = Factura.objects.create(venta=venta)

        return CrearFacturaMutation(factura=factura)

class EditarFacturaMutation(graphene.Mutation):
    class Arguments:
        factura_id = graphene.ID(required=True)
        venta_id = graphene.ID()

    factura = graphene.Field(FacturaType)

    def mutate(self, info, factura_id, venta_id=None):
        try:
            # Obtener la factura a partir del ID
            factura = Factura.objects.get(id=factura_id)

            # Actualizar la venta si se proporciona un nuevo ID de venta
            if venta_id:
                venta = Venta.objects.get(id=venta_id)
                factura.venta = venta

            # Guardar los cambios en la factura
            factura.save()

            return EditarFacturaMutation(factura=factura)
        except Factura.DoesNotExist:
            return EditarFacturaMutation(factura=None)

class EliminarFacturaMutation(graphene.Mutation):
    class Arguments:
        factura_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, factura_id):
        try:
            # Obtener la factura a partir del ID
            factura = Factura.objects.get(id=factura_id)

            # Eliminar la factura
            factura.delete()

            success = True
        except Factura.DoesNotExist:
            success = False

        return EliminarFacturaMutation(success=success)

class FacturaMutation(graphene.ObjectType):
    crear_factura = CrearFacturaMutation.Field()
    editar_factura = EditarFacturaMutation.Field()
    eliminar_factura = EliminarFacturaMutation.Field()

