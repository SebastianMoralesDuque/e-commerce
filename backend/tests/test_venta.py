from django.test import TestCase
from app.graphql.schema import schema
from app.models import Ciudad, User, Carrito,Categoria,Producto,ItemCarrito,MetodoPago,Venta
from decimal import Decimal


class VentaMutationTestCase(TestCase):
    
    def test_crear_venta_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago= MetodoPago.objects.create(nombre="metodo de pago de prueba")
        # Crear un item de carrito
        item_carrito = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=5)

        # Definir la consulta de mutación para crear una venta
        mutation = '''
            mutation {
                crearVenta(
                    carritoId: "%s",
                    metodoPagoId: "%s",
                    precioTotal: "10.99",
                    usuarioId: "%s"
                ) {
                    venta {
                        id
                    }
                }
            }
        ''' % (str(carrito.id), (str(metodo_pago.id)), str(user.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('crearVenta', result['data'])
        self.assertIn('venta', result['data']['crearVenta'])
        venta = result['data']['crearVenta']['venta']

        # Verificar que se haya creado la venta en la base de datos
        self.assertTrue(Venta.objects.filter(id=venta['id']).exists())


    def test_editar_venta_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago = MetodoPago.objects.create(nombre="metodo de pago de prueba")
        # Crear una venta
        venta = Venta.objects.create(usuario=user, carrito=carrito, metodo_pago=metodo_pago, precio_total=10.99)

        # Definir la consulta de mutación para editar una venta
        mutation = '''
            mutation {
                editarVenta(
                    ventaId: "%s",
                    carritoId: "%s",
                    metodoPagoId: "%s",
                    precioTotal: "15.99",
                    usuarioId: "%s"
                ) {
                    venta {
                        id
                        precioTotal
                    }
                }
            }
        ''' % (str(venta.id), str(carrito.id), str(metodo_pago.id), str(user.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('editarVenta', result['data'])
        self.assertIn('venta', result['data']['editarVenta'])
        venta = result['data']['editarVenta']['venta']

        # Verificar que la venta se haya editado en la base de datos
        venta_db = Venta.objects.get(id=venta['id'])
        self.assertEqual(venta_db.precio_total, Decimal('15.99'))


    def test_eliminar_venta_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)
        metodo_pago = MetodoPago.objects.create(nombre="metodo de pago de prueba")
        # Crear una venta
        venta = Venta.objects.create(usuario=user, carrito=carrito, metodo_pago=metodo_pago, precio_total=10.99)

        # Definir la consulta de mutación para eliminar una venta
        mutation = '''
            mutation {
                eliminarVenta(ventaId: "%s") {
                    success
                }
            }
        ''' % str(venta.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {'query': mutation})

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('eliminarVenta', result['data'])
        self.assertTrue(result['data']['eliminarVenta']['success'])

        # Verificar que la venta se haya eliminado de la base de datos
        self.assertFalse(Venta.objects.filter(id=venta.id).exists())
