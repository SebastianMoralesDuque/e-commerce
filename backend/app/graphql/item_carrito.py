import graphene
from graphene_django import DjangoObjectType
from ..models import ItemCarrito

class ItemCarritoType(DjangoObjectType):
    class Meta:
        model = ItemCarrito

import graphene
from graphene_django import DjangoObjectType
from ..models import ItemCarrito, Carrito, Producto

class ItemCarritoType(DjangoObjectType):
    class Meta:
        model = ItemCarrito

class CreateItemCarrito(graphene.Mutation):
    item_carrito = graphene.Field(ItemCarritoType)

    class Arguments:
        carrito_id = graphene.ID(required=True)
        producto_id = graphene.ID(required=True)
        cantidad = graphene.Int(required=True)

    def mutate(self, info, carrito_id, producto_id, cantidad):
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            producto = Producto.objects.get(id=producto_id)
        except Carrito.DoesNotExist or Producto.DoesNotExist:
            raise Exception("El Carrito o el Producto no existen.")

        item_carrito = ItemCarrito(carrito=carrito, producto=producto, cantidad=cantidad)
        item_carrito.save()

        return CreateItemCarrito(item_carrito=item_carrito)

class DeleteItemCarrito(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            item_carrito = ItemCarrito.objects.get(id=id)
            item_carrito.delete()
            success = True
        except ItemCarrito.DoesNotExist:
            success = False

        return DeleteItemCarrito(success=success)

class UpdateItemCarrito(graphene.Mutation):
    item_carrito = graphene.Field(ItemCarritoType)

    class Arguments:
        id = graphene.ID(required=True)
        cantidad = graphene.Int()

    def mutate(self, info, id, cantidad=None):
        try:
            item_carrito = ItemCarrito.objects.get(id=id)

            if cantidad is not None:
                item_carrito.cantidad = cantidad

            item_carrito.save()

            return UpdateItemCarrito(item_carrito=item_carrito)
        except ItemCarrito.DoesNotExist:
            return None

class ItemCarritoMutation(graphene.ObjectType):
    create_item_carrito = CreateItemCarrito.Field()
    delete_item_carrito = DeleteItemCarrito.Field()
    update_item_carrito = UpdateItemCarrito.Field()

class ItemCarritoQuery(graphene.ObjectType):
    items_carrito = graphene.List(ItemCarritoType)
    item_carrito_by_id = graphene.Field(ItemCarritoType, id=graphene.ID(required=True))

    def resolve_items_carrito(self, info):
        return ItemCarrito.objects.all()

    def resolve_item_carrito_by_id(self, info, id):
        try:
            return ItemCarrito.objects.get(id=id)
        except ItemCarrito.DoesNotExist:
            return None
