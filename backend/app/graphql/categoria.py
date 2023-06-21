import graphene
from graphene_django import DjangoObjectType
from ..models import Categoria

class CategoriaType(DjangoObjectType):
    class Meta:
        model = Categoria

class CreateCategoriaMutation(graphene.Mutation):
    categoria = graphene.Field(CategoriaType)

    class Arguments:
        nombre = graphene.String(required=True)

    def mutate(self, info, nombre):
        categoria = Categoria(nombre=nombre)
        categoria.save()

        return CreateCategoriaMutation(categoria=categoria)

class UpdateCategoriaMutation(graphene.Mutation):
    categoria = graphene.Field(CategoriaType)

    class Arguments:
        id = graphene.ID(required=True)
        nombre = graphene.String()

    def mutate(self, info, id, nombre):
        categoria = Categoria.objects.get(id=id)

        if nombre:
            categoria.nombre = nombre

        categoria.save()

        return UpdateCategoriaMutation(categoria=categoria)

class DeleteCategoriaMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        categoria = Categoria.objects.get(id=id)
        categoria.delete()

        return DeleteCategoriaMutation(success=True)

class CategoriaMutation(graphene.ObjectType):
    create_categoria = CreateCategoriaMutation.Field()
    update_categoria = UpdateCategoriaMutation.Field()
    delete_categoria = DeleteCategoriaMutation.Field()

class CategoriaQuery(graphene.ObjectType):
    categorias = graphene.List(CategoriaType)

    def resolve_categorias(self, info):
        return Categoria.objects.all()

