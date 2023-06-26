from django.test import TestCase
from django.contrib.auth.models import User
from graphene.test import Client
from app.graphql.schema import schema
from app.models import Ciudad, User, Carrito,Categoria,Producto,MetodoPago,Venta,Factura
import datetime

class FacturaMutationTest(TestCase):

    def test_crear_factura_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago = MetodoPago.objects.create(nombre="metodo de pago de prueba")
        venta = Venta.objects.create(usuario=user, carrito=carrito, metodo_pago=metodo_pago, precio_total=10.99)

        # Definir la consulta de mutación para crear una factura
        mutation = '''
            mutation {
                crearFactura(
                    ventaId: "%s"
                ) {
                    factura {
                        id
                        fecha
                    }
                }
            }
        ''' % (str(venta.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('crearFactura', result['data'])
        self.assertIn('factura', result['data']['crearFactura'])
        factura = result['data']['crearFactura']['factura']

        # Verificar que se haya creado la factura en la base de datos
        self.assertTrue(Factura.objects.filter(id=factura['id']).exists())


    def test_editar_factura_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago = MetodoPago.objects.create(nombre="metodo de pago de prueba")
        venta = Venta.objects.create(usuario=user, carrito=carrito, metodo_pago=metodo_pago, precio_total=10.99)
        factura = Factura.objects.create(venta=venta, fecha=datetime.datetime.now())

        # Definir la consulta de mutación para editar una factura
        mutation = '''
            mutation {
                editarFactura(
                    facturaId: "%s",
                    ventaId: "%s",
                ) {
                    factura {
                        id
                        fecha
                    }
                }
            }
        ''' % (str(factura.id), str(venta.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('editarFactura', result['data'])
        self.assertIn('factura', result['data']['editarFactura'])
        factura = result['data']['editarFactura']['factura']


    def test_eliminar_factura_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago = MetodoPago.objects.create(nombre="metodo de pago de prueba")
        venta = Venta.objects.create(usuario=user, carrito=carrito, metodo_pago=metodo_pago, precio_total=10.99)
        factura = Factura.objects.create(venta=venta)

        # Definir la consulta de mutación para eliminar una factura
        mutation = '''
            mutation {
                eliminarFactura(facturaId: "%s") {
                    success
                }
            }
        ''' % (str(factura.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('eliminarFactura', result['data'])
        eliminar_factura_result = result['data']['eliminarFactura']

        # Verificar que la factura se haya eliminado de la base de datos
        self.assertTrue(eliminar_factura_result['success'])
        self.assertFalse(Factura.objects.filter(id=factura.id).exists())