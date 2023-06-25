from django.test import TestCase
from app.graphql.schema import schema
from app.models import Ciudad, User, Carrito,Categoria,Producto,ItemCarrito


class CarritoMutationTestCase(TestCase):
    def test_create_carrito_mutation(self):
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        # Crear un usuario de prueba en la base de datos
        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            ciudad=ciudad,
            direccion='Dirección de prueba'
        )

        mutation = '''
            mutation {
                createCarrito(usuarioId: %s) {
                    carrito {
                        id
                    }
                }
            }
        ''' % user.id

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()

        self.assertIsNotNone(result['data']['createCarrito']['carrito'])
        self.assertIsInstance(result['data']['createCarrito']['carrito']['id'], str)

    def test_update_carrito_mutation(self):
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        # Crear un usuario de prueba en la base de datos
        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            ciudad=ciudad,
            direccion='Dirección de prueba'
        )

        carrito = Carrito.objects.create(usuario=user)


        mutation = '''
            mutation {
                updateCarrito(carritoId: %s, usuarioId: %s) {
                    carrito {
                        id
                    }
                }
            }
        ''' %  (carrito.id, user.id)

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()

        self.assertIsNotNone(result['data']['updateCarrito']['carrito'])
        self.assertIsInstance(result['data']['updateCarrito']['carrito']['id'], str)
        
    def test_delete_carrito_mutation(self):
        ciudad = Ciudad.objects.create(nombre='Ciudad')

        # Create a test user in the database
        user = User.objects.create(
            email='user@gmail.com',
            password='user123',
            is_admin=False,
            ciudad=ciudad,
            direccion='Dirección de user'
        )

        # Create a test carrito associated with the user
        carrito = Carrito.objects.create(usuario=user)

        mutation = '''
            mutation {
                deleteCarrito(carritoId: %s) {
                    success
                }
            }
        ''' % carrito.id

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()

        self.assertTrue(result['data']['deleteCarrito']['success'])


    def test_create_item_carrito(self):
        # Crear objetos necesarios para el test
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)

        mutation = '''
            mutation {
                createItemCarrito(carritoId: "%s", productoId: "%s", cantidad: 5) {
                    itemCarrito {
                        id
                        cantidad
                    }
                }
            }
        ''' % (str(carrito.id), str(producto.id))

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()
        self.assertIn('data', result)
        self.assertIn('createItemCarrito', result['data'])
        self.assertIn('itemCarrito', result['data']['createItemCarrito'])
        item_carrito = result['data']['createItemCarrito']['itemCarrito']
        self.assertIsNotNone(item_carrito)
        self.assertIn('id', item_carrito)
        self.assertIn('cantidad', item_carrito)
        self.assertEqual(item_carrito['cantidad'], 5)


    def test_update_item_carrito(self):
        # Crear objetos necesarios para el test
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)

        # Crear un item de carrito
        item_carrito = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=5)

        # Realizar la mutación de actualización
        mutation = '''
            mutation {
                updateItemCarrito(itemCarritoId: "%s", cantidad: 8) {
                    itemCarrito {
                        id
                        cantidad
                    }
                }
            }
        ''' % str(item_carrito.id)

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()

        # Verificar que la respuesta contiene el campo 'data'
        self.assertIn('data', result)

        # Verificar que 'data' contiene 'updateItemCarrito'
        self.assertIn('updateItemCarrito', result['data'])

        # Verificar que 'updateItemCarrito' contiene 'itemCarrito'
        self.assertIn('itemCarrito', result['data']['updateItemCarrito'])

        # Obtener el objeto 'itemCarrito' de la respuesta
        updated_item_carrito = result['data']['updateItemCarrito']['itemCarrito']

        # Verificar que 'itemCarrito' no es None
        self.assertIsNotNone(updated_item_carrito)

        # Verificar que 'itemCarrito' contiene 'id'
        self.assertIn('id', updated_item_carrito)

        # Verificar que 'itemCarrito' contiene 'cantidad'
        self.assertIn('cantidad', updated_item_carrito)

        # Verificar que 'cantidad' es igual a 8
        self.assertEqual(updated_item_carrito['cantidad'], 8)


    def test_delete_item_carrito(self):
        # Crear objetos necesarios para el test
        categoria = Categoria.objects.create(nombre='Electrónica')
        producto = Producto.objects.create(nombre='Producto 1', categoria=categoria, imagen='ruta/imagen.jpg', stock=10, precio=9.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad 1')
        user = User.objects.create_user(email='usuario1@example.com', password='password123', is_admin=False, direccion='Calle 123', ciudad=ciudad)
        carrito = Carrito.objects.create(usuario=user)

        # Crear un item de carrito
        item_carrito = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=5)

        # Realizar la mutación de eliminación
        mutation = '''
            mutation {
                deleteItemCarrito(itemCarritoId: "%s") {
                    success
                }
            }
        ''' % str(item_carrito.id)

        response = self.client.post('/graphql/', {
            'query': mutation,
        })
        result = response.json()

        # Verificar que la respuesta contiene el campo 'data'
        self.assertIn('data', result)

        # Verificar que 'data' contiene 'deleteItemCarrito'
        self.assertIn('deleteItemCarrito', result['data'])

        # Obtener el resultado de la eliminación
        deletion_result = result['data']['deleteItemCarrito']

        # Verificar que 'deleteItemCarrito' contiene 'success'
        self.assertIn('success', deletion_result)

        # Verificar que 'success' es True (éxito en la eliminación)
        self.assertTrue(deletion_result['success'])
