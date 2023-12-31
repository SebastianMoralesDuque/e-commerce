import graphene
from .user import UserQuery, UserMutation
from .ciudad import CiudadQuery, CiudadMutation
from .categoria import CategoriaQuery, CategoriaMutation
from .producto import ProductoQuery, ProductoMutation
from .carrito import CarritoQuery, CarritoMutation
from .item_carrito import ItemCarritoQuery, ItemCarritoMutation
from .metodo_pago import MetodoPagoQuery, MetodoPagoMutation
from .resena import ResenaQuery,ResenaMutation
from .venta import VentaQuery,VentaMutation
from .factura import FacturaQuery,FacturaMutation

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
    ResenaMutation,
    VentaMutation,
    FacturaMutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
