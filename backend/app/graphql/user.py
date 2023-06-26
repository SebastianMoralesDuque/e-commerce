import graphene
from graphene_django import DjangoObjectType
from ..models import User, Ciudad

class UserType(DjangoObjectType):
    class Meta:
        model = User

class CreateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        is_admin = graphene.Boolean(required=True)
        direccion = graphene.String(required=True)
        ciudad_id = graphene.Int(required=True)

    def mutate(self, info, password, email, is_admin, direccion, ciudad_id):
        ciudad = Ciudad.objects.get(id=ciudad_id)

        user = User(
            password=password,
            email=email,
            is_admin=is_admin,
            direccion=direccion,
            ciudad=ciudad
        )
        user.save()

        return CreateUserMutation(user=user)

class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        password = graphene.String()
        email = graphene.String()
        is_admin = graphene.Boolean()
        direccion = graphene.String()
        ciudad_id = graphene.Int()

    def mutate(self, info, id, **kwargs):
        user = User.objects.get(id=id)

        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        
        user.save()

        return UpdateUserMutation(user=user)

class DeleteUserMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = User.objects.get(id=id)
        user.delete()

        return DeleteUserMutation(success=True)

class UserMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()

class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
