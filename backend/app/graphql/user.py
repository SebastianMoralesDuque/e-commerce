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
        direccion = graphene.String(required=True)
        ciudad_id = graphene.Int(required=True)
        is_admin = graphene.Boolean(required=True)

    def mutate(self, info, password, email, direccion, ciudad_id, is_admin):
        ciudad = Ciudad.objects.get(id=ciudad_id)

        user = User(
            email=email,
            direccion=direccion,
            ciudad=ciudad,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save()

        return CreateUserMutation(user=user)

class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()
        direccion = graphene.String()
        ciudad_id = graphene.Int()
        is_admin = graphene.Boolean()

    def mutate(self, info, id, **kwargs):
        user = User.objects.get(id=id)

        for key, value in kwargs.items():
            if value is not None:
                if key == 'password':
                    user.set_password(value)
                elif key == 'ciudad_id':
                    ciudad = Ciudad.objects.get(id=value)
                    setattr(user, 'ciudad', ciudad)
                else:
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
        return User.objects.get(id=id)

schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
