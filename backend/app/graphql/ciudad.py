import graphene
from graphene_django import DjangoObjectType
from ..models import Ciudad

class CiudadType(DjangoObjectType):
    class Meta:
        model = Ciudad

class CreateCiudadMutation(graphene.Mutation):
    ciudad = graphene.Field(CiudadType)

    class Arguments:
        nombre = graphene.String(required=True)

    def mutate(self, info, nombre):
        # Crea una nueva instancia del modelo Ciudad con el nombre proporcionado
        ciudad = Ciudad(nombre=nombre)
        ciudad.save()

        # Devuelve la instancia creada
        return CreateCiudadMutation(ciudad=ciudad)

class UpdateCiudadMutation(graphene.Mutation):
    ciudad = graphene.Field(CiudadType)

    class Arguments:
        id = graphene.ID(required=True)
        nombre = graphene.String(required=True)

    def mutate(self, info, id, nombre):
        # Obtiene la ciudad a actualizar
        ciudad = Ciudad.objects.get(id=id)

        # Actualiza el nombre de la ciudad
        ciudad.nombre = nombre
        ciudad.save()

        # Devuelve la instancia actualizada
        return UpdateCiudadMutation(ciudad=ciudad)

class DeleteCiudadMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        # Obtiene la ciudad a eliminar
        ciudad = Ciudad.objects.get(id=id)

        # Elimina la ciudad
        ciudad.delete()

        # Devuelve un indicador de éxito
        return DeleteCiudadMutation(success=True)

class CiudadMutation(graphene.ObjectType):
    create_ciudad = CreateCiudadMutation.Field()
    update_ciudad = UpdateCiudadMutation.Field()
    delete_ciudad = DeleteCiudadMutation.Field()

class CiudadQuery(graphene.ObjectType):
    ciudades = graphene.List(CiudadType)

    def resolve_ciudades(self, info):
        return Ciudad.objects.all()

