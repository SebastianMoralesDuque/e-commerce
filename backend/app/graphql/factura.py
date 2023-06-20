import graphene
from graphene_django import DjangoObjectType
from ..models import Factura

class FacturaType(DjangoObjectType):
    class Meta:
        model = Factura

class FacturaQuery(graphene.ObjectType):
    facturas = graphene.List(FacturaType)

    def resolve_facturas(self, info):
        return Factura.objects.all()
