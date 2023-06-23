from django.test import TestCase
from app.graphql.schema import schema
from app.models import Ciudad, User


class UserMutationTest(TestCase):
    
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

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('createUser', data)
        create_user_result = data['createUser']
        self.assertIsNotNone(create_user_result)  # Verificar si create_user_result no es None
        if create_user_result:
            self.assertIn('user', create_user_result)
            user = create_user_result['user']
            self.assertEqual(user['email'], 'pruebausuario@gmail.com')

            # Verificar que se haya creado el usuario en la base de datos
            self.assertTrue(User.objects.filter(email='pruebausuario@gmail.com').exists())

    def test_update_user_mutation(self):
        # Crear una ciudad de prueba en la base de datos
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        # Crear un usuario de prueba en la base de datos
        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            ciudad=ciudad,
            direccion='Dirección de prueba'
        )

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                updateUser(
                    id: %d,
                    email: "modific@gmail.com",
                    password: "modificad",
                    isAdmin: true,
                    direccion: "modiifcada",
                    ciudadId: %d
                ) {
                    user {
                        email
                    }
                }
            }
        ''' % (user.id, ciudad.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('updateUser', data)
        update_user_result = data['updateUser']
        self.assertIsNotNone(update_user_result)  # Verificar si update_user_result no es None
        if update_user_result:
            self.assertIn('user', update_user_result)
            updated_user = update_user_result['user']
            self.assertEqual(updated_user['email'], 'modific@gmail.com')

            # Verificar que el usuario se haya actualizado en la base de datos
            user_db = User.objects.get(id=user.id)
            self.assertEqual(user_db.email, 'modific@gmail.com')
            self.assertEqual(user_db.password, 'modificad')
            self.assertEqual(user_db.is_admin, True)
            self.assertEqual(user_db.direccion, 'modiifcada')
            self.assertEqual(user_db.ciudad_id, ciudad.id)

    def test_delete_user_mutation(self):
        # Crear una ciudad de prueba en la base de datos
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        # Crear un usuario de prueba en la base de datos
        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            ciudad=ciudad,
            direccion='Dirección de prueba'
        )

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                deleteUser(
                    id: %d
                ) {
                    success
                }
            }
        ''' % user.id

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('deleteUser', data)
        delete_user_result = data['deleteUser']
        self.assertIsNotNone(delete_user_result)  # Verificar si delete_user_result no es None
        if delete_user_result:
            self.assertTrue(delete_user_result['success'])

            # Verificar que el usuario se haya eliminado de la base de datos
            self.assertFalse(User.objects.filter(id=user.id).exists())