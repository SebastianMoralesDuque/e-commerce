import graphene
from graphene_django import DjangoObjectType
from ..models import MetodoPago

class MetodoPagoType(DjangoObjectType):
    class Meta:
        model = MetodoPago

class CreateMetodoPagoMutation(graphene.Mutation):
    metodo_pago = graphene.Field(MetodoPagoType)

    class Arguments:
        nombre = graphene.String(required=True)

    def mutate(self, info, nombre):
        metodo_pago = MetodoPago(nombre=nombre)
        metodo_pago.save()

        return CreateMetodoPagoMutation(metodo_pago=metodo_pago)

class UpdateMetodoPagoMutation(graphene.Mutation):
    metodo_pago = graphene.Field(MetodoPagoType)

    class Arguments:
        id = graphene.ID(required=True)
        nombre = graphene.String()

    def mutate(self, info, id, **kwargs):
        metodo_pago = MetodoPago.objects.get(id=id)

        for key, value in kwargs.items():
            if value is not None:
                setattr(metodo_pago, key, value)
        
        metodo_pago.save()

        return UpdateMetodoPagoMutation(metodo_pago=metodo_pago)

class DeleteMetodoPagoMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        metodo_pago = MetodoPago.objects.get(id=id)
        metodo_pago.delete()

        return DeleteMetodoPagoMutation(success=True)

class MetodoPagoMutation(graphene.ObjectType):
    create_metodo_pago = CreateMetodoPagoMutation.Field()
    update_metodo_pago = UpdateMetodoPagoMutation.Field()
    delete_metodo_pago = DeleteMetodoPagoMutation.Field()

class MetodoPagoQuery(graphene.ObjectType):
    metodos_pago = graphene.List(MetodoPagoType)

    def resolve_metodos_pago(self, info):
        return MetodoPago.objects.all()
