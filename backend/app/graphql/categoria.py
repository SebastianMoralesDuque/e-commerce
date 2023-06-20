import graphene
from graphene_django import DjangoObjectType
from ..models import Categoria

class CategoriaType(DjangoObjectType):
    class Meta:
        model = Categoria

class CategoriaQuery(graphene.ObjectType):
    categorias = graphene.List(CategoriaType)

    def resolve_categorias(self, info):
        return Categoria.objects.all()
