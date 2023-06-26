import graphene
from graphene_django import DjangoObjectType
from ..models import Resena

class ResenaType(DjangoObjectType):
    class Meta:
        model = Resena


class ResenaInput(graphene.InputObjectType):
    usuario_id = graphene.ID(required=True)
    producto_id = graphene.ID(required=True)
    contenido = graphene.String(required=True)
    calificacion = graphene.Float(required=True)

class CreateResenaMutation(graphene.Mutation):
    resena = graphene.Field(ResenaType)

    class Arguments:
        input = ResenaInput(required=True)

    def mutate(self, info, input):
        # Obtener los datos del input
        usuario_id = input.usuario_id
        producto_id = input.producto_id
        contenido = input.contenido
        calificacion = input.calificacion

        # Crear la reseña
        resena = Resena(
            usuario_id=usuario_id,
            producto_id=producto_id,
            contenido=contenido,
            calificacion=calificacion
        )
        resena.save()

        return CreateResenaMutation(resena=resena)

class DeleteResenaMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        resena_id = graphene.ID(required=True)

    def mutate(self, info, resena_id):
        # Obtener la reseña por su ID
        try:
            resena = Resena.objects.get(pk=resena_id)
            # Eliminar la reseña
            resena.delete()
            return DeleteResenaMutation(success=True)
        except Resena.DoesNotExist:
            return DeleteResenaMutation(success=False)

class UpdateResenaMutation(graphene.Mutation):
    resena = graphene.Field(ResenaType)

    class Arguments:
        resena_id = graphene.ID(required=True)
        input = ResenaInput(required=True)

    def mutate(self, info, resena_id, input):
        # Obtener la reseña por su ID
        try:
            resena = Resena.objects.get(pk=resena_id)
        except Resena.DoesNotExist:
            raise Exception("La reseña no existe")

        # Obtener los datos del input
        usuario_id = input.usuario_id
        producto_id = input.producto_id
        contenido = input.contenido
        calificacion = input.calificacion

        # Actualizar los campos de la reseña
        resena.usuario_id = usuario_id
        resena.producto_id = producto_id
        resena.contenido = contenido
        resena.calificacion = calificacion
        resena.save()

        return UpdateResenaMutation(resena=resena)

class ResenaMutation(graphene.ObjectType):
    create_resena = CreateResenaMutation.Field()
    delete_resena = DeleteResenaMutation.Field()
    update_resena = UpdateResenaMutation.Field()

class ResenaQuery(graphene.ObjectType):
    resenas = graphene.List(ResenaType)
    resena_by_id = graphene.Field(ResenaType, id=graphene.ID(required=True))

    def resolve_resenas(self, info):
        return Resena.objects.all()

    def resolve_resena_by_id(self, info, id):
        try:
            return Resena.objects.get(id=id)
        except Resena.DoesNotExist:
            return None