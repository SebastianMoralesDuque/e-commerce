from django.test import TestCase
from app.graphql.schema import schema
from app.models import Ciudad, User, Carrito


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
