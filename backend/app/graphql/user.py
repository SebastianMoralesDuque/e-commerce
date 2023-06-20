import graphene
from graphene_django import DjangoObjectType
from ..models import User
from .ciudad import CiudadType

class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))
    users_by_ciudad = graphene.List(UserType, ciudad=graphene.String(required=True))

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)

    def resolve_users_by_ciudad(self, info, ciudad):
        return User.objects.filter(ciudad__nombre=ciudad)
