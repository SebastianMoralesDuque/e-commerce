import graphene
from .user import UserQuery
from .ciudad import CiudadQuery, CiudadMutation
from .categoria import CategoriaQuery
from .producto import ProductoQuery
from .carrito import CarritoQuery
from .item_carrito import ItemCarritoQuery
from .metodo_pago import MetodoPagoQuery
from .resena import ResenaQuery
from .venta import VentaQuery
from .factura import FacturaQuery

class Query(
    UserQuery,
    CiudadQuery,
    CategoriaQuery,
    ProductoQuery,
    CarritoQuery,
    ItemCarritoQuery,
    MetodoPagoQuery,
    ResenaQuery,
    VentaQuery,
    FacturaQuery,
    graphene.ObjectType,
):
    pass

class Mutation(
    CiudadMutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
