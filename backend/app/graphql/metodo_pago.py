import graphene
from graphene_django import DjangoObjectType
from ..models import MetodoPago

class MetodoPagoType(DjangoObjectType):
    class Meta:
        model = MetodoPago

class MetodoPagoQuery(graphene.ObjectType):
    metodos_pago = graphene.List(MetodoPagoType)

    def resolve_metodos_pago(self, info):
        return MetodoPago.objects.all()
