import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..models import Producto, Categoria

class CategoriaType(DjangoObjectType):
    class Meta:
        model = Categoria

class ProductoType(DjangoObjectType):
    class Meta:
        model = Producto

class CreateProductoMutation(graphene.Mutation):
    producto = graphene.Field(ProductoType)

    class Arguments:
        nombre = graphene.String(required=True)
        categoria_id = graphene.Int(required=True)
        imagen = graphene.Upload(required=True)  # Actualizado a Upload
        stock = graphene.Int(required=True)

    def mutate(self, info, nombre, categoria_id, imagen, stock):
        categoria = Categoria.objects.get(id=categoria_id)

        producto = Producto(
            nombre=nombre,
            categoria=categoria,
            stock=stock
        )
        producto.imagen.save(imagen.name, imagen, save=True) 

        return CreateProductoMutation(producto=producto)

class UpdateProductoMutation(graphene.Mutation):
    producto = graphene.Field(ProductoType)

    class Arguments:
        id = graphene.ID(required=True)
        nombre = graphene.String()
        categoria_id = graphene.Int()
        imagen = graphene.String()
        stock = graphene.Int()

    def mutate(self, info, id, **kwargs):
        producto = Producto.objects.get(id=id)

        categoria_id = kwargs.get('categoria_id')
        if categoria_id is not None:
            categoria = Categoria.objects.get(id=categoria_id)
            kwargs['categoria'] = categoria
            del kwargs['categoria_id']

        for key, value in kwargs.items():
            if value is not None:
                setattr(producto, key, value)
        
        producto.save()

        return UpdateProductoMutation(producto=producto)

class DeleteProductoMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        producto = Producto.objects.get(id=id)
        producto.delete()

        return DeleteProductoMutation(success=True)

class ProductoMutation(graphene.ObjectType):
    create_producto = CreateProductoMutation.Field()
    update_producto = UpdateProductoMutation.Field()
    delete_producto = DeleteProductoMutation.Field()

class ProductoQuery(graphene.ObjectType):
    productos = graphene.List(ProductoType)
    producto_by_id = graphene.Field(ProductoType, id=graphene.ID(required=True))

    def resolve_productos(self, info):
        return Producto.objects.all()
    
    def resolve_producto_by_id(self, info, id):
        return Producto.objects.get(id=id)
