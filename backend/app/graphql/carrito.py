import graphene
from graphene_django import DjangoObjectType
from ..models import Carrito, ItemCarrito, Producto

class CarritoType(DjangoObjectType):
    class Meta:
        model = Carrito

class ItemCarritoType(DjangoObjectType):
    class Meta:
        model = ItemCarrito

class CarritoQuery(graphene.ObjectType):
    carritos = graphene.List(CarritoType)

    def resolve_carritos(self, info):
        return Carrito.objects.all()

class CreateCarritoMutation(graphene.Mutation):
    carrito = graphene.Field(CarritoType)

    class Arguments:
        usuario_id = graphene.ID(required=True)

    def mutate(self, info, usuario_id):
        carrito = Carrito(usuario_id=usuario_id)
        carrito.save()

        return CreateCarritoMutation(carrito=carrito)

class UpdateCarritoMutation(graphene.Mutation):
    carrito = graphene.Field(CarritoType)

    class Arguments:
        carrito_id = graphene.ID(required=True)
        usuario_id = graphene.ID(required=False)

    def mutate(self, info, carrito_id, usuario_id=None):
        carrito = Carrito.objects.get(id=carrito_id)

        if usuario_id is not None:
            carrito.usuario_id = usuario_id

        carrito.save()

        return UpdateCarritoMutation(carrito=carrito)

class DeleteCarritoMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        carrito_id = graphene.ID(required=True)

    def mutate(self, info, carrito_id):
        carrito = Carrito.objects.get(id=carrito_id)
        carrito.delete()

        return DeleteCarritoMutation(success=True)

class AddProductoToCarritoMutation(graphene.Mutation):
    carrito = graphene.Field(CarritoType)

    class Arguments:
        carrito_id = graphene.ID(required=True)
        producto_id = graphene.ID(required=True)
        cantidad = graphene.Int(required=True)

    def mutate(self, info, carrito_id, producto_id, cantidad):
        carrito = Carrito.objects.get(id=carrito_id)
        producto = Producto.objects.get(id=producto_id)

        item_carrito = ItemCarrito(carrito=carrito, producto=producto, cantidad=cantidad)
        item_carrito.save()

        return AddProductoToCarritoMutation(carrito=carrito)

class UpdateItemCarritoMutation(graphene.Mutation):
    item_carrito = graphene.Field(ItemCarritoType)

    class Arguments:
        item_carrito_id = graphene.ID(required=True)
        cantidad = graphene.Int(required=True)

    def mutate(self, info, item_carrito_id, cantidad):
        item_carrito = ItemCarrito.objects.get(id=item_carrito_id)
        item_carrito.cantidad = cantidad
        item_carrito.save()

        return UpdateItemCarritoMutation(item_carrito=item_carrito)

class DeleteItemCarritoMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        item_carrito_id = graphene.ID(required=True)

    def mutate(self, info, item_carrito_id):
        item_carrito = ItemCarrito.objects.get(id=item_carrito_id)
        item_carrito.delete()

        return DeleteItemCarritoMutation(success=True)

class CarritoMutation(graphene.ObjectType):
    create_carrito = CreateCarritoMutation.Field()
    update_carrito = UpdateCarritoMutation.Field()
    delete_carrito = DeleteCarritoMutation.Field()
    add_producto_to_carrito = AddProductoToCarritoMutation.Field()
    update_item_carrito = UpdateItemCarritoMutation.Field()
    delete_item_carrito = DeleteItemCarritoMutation.Field()

class CarritoQuery(graphene.ObjectType):
    carritos = graphene.List(CarritoType)

    def resolve_carritos(self, info):
        return Carrito.objects.all()
