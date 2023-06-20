import graphene
from graphene_django import DjangoObjectType
from ..models import Carrito

class CarritoType(DjangoObjectType):
    class Meta:
        model = Carrito

class CarritoQuery(graphene.ObjectType):
    carritos = graphene.List(CarritoType)

    def resolve_carritos(self, info):
        return Carrito.objects.all()
