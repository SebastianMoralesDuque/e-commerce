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
