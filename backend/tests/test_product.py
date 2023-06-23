from django.test import TestCase
from graphene.test import Client
from app.graphql.schema import schema
from app.models import Ciudad, User


class UserMutationTest(TestCase):
    def setUp(self):
        # Configurar los datos de prueba necesarios
        self.client = Client(schema)

    def test_create_user_mutation(self):
        # Crear una ciudad de prueba en la base de datos
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                createUser(
                    email: "pruebausuario@gmail.com",
                    password: "usuario123",
                    isAdmin: false,
                    direccion: "calle 222",
                    ciudadId: %d
                ) {
                    user {
                        id
                        email
                    }
                }
            }
        ''' % ciudad.id

        # Ejecutar la mutación utilizando el cliente de pruebas de GraphQL
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', executed)
        self.assertIn('createUser', executed['data'])
        self.assertIn('user', executed['data']['createUser'])
        user = executed['data']['createUser']['user']
        self.assertEqual(user['email'], 'pruebausuario@gmail.com')

        # Verificar que se haya creado el usuario en la base de datos
        self.assertTrue(User.objects.filter(email='pruebausuario@gmail.com').exists())

        # Obtener el usuario de la base de datos
        user_db = User.objects.get(email='pruebausuario@gmail.com')

        # Realizar una prueba de eliminación de usuario
        mutation = '''
            mutation {
                deleteUser(id: %d) {
                    success
                }
            }
        ''' % user_db.id

        # Ejecutar la mutación para eliminar el usuario
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación de eliminación
        self.assertNotIn('errors', executed)
        self.assertIn('deleteUser', executed['data'])
        self.assertTrue(executed['data']['deleteUser']['success'])
