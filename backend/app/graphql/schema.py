import graphene
from .user import UserQuery, UserMutation
from .ciudad import CiudadQuery, CiudadMutation
from .categoria import CategoriaQuery, CategoriaMutation
from .producto import ProductoQuery, ProductoMutation
from .carrito import CarritoQuery, CarritoMutation
from .item_carrito import ItemCarritoQuery, ItemCarritoMutation
from .metodo_pago import MetodoPagoQuery, MetodoPagoMutation
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
    UserMutation,
    CategoriaMutation,
    MetodoPagoMutation,
    ProductoMutation,
    CarritoMutation,
    ItemCarritoMutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
