import graphene
from graphene_django import DjangoObjectType
from ..models import Resena

class ResenaType(DjangoObjectType):
    class Meta:
        model = Resena

class ResenaQuery(graphene.ObjectType):
    resenas = graphene.List(ResenaType)

    def resolve_resenas(self, info):
        return Resena.objects.all()
