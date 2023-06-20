import graphene
from graphene_django import DjangoObjectType
from ..models import ItemCarrito

class ItemCarritoType(DjangoObjectType):
    class Meta:
        model = ItemCarrito

class ItemCarritoQuery(graphene.ObjectType):
    item_carritos = graphene.List(ItemCarritoType)

    def resolve_item_carritos(self, info):
        return ItemCarrito.objects.all()
