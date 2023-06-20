import graphene
from graphene_django import DjangoObjectType
from ..models import Producto

class ProductoType(DjangoObjectType):
    class Meta:
        model = Producto

class ProductoQuery(graphene.ObjectType):
    productos = graphene.List(ProductoType)
    producto_by_id = graphene.Field(ProductoType, id=graphene.Int(required=True))

    def resolve_productos(self, info):
        return Producto.objects.all()
    
    def resolve_producto_by_id(self, info, id):
        return Producto.objects.get(id=id)