from django.test import Client, TestCase
from app.graphql.schema import schema
from app.models import Ciudad

class CiudadMutationTest(TestCase):
    def setUp(self):
        # Configurar los datos de prueba necesarios
        self.client = Client()

    def test_create_ciudad_mutation(self):
        # Definir la consulta de mutación
        mutation = '''
            mutation {
                createCiudad(nombre: "Ciudad de prueba") {
                    ciudad {
                        id
                        nombre
                    }
                }
            }
        '''

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('createCiudad', result['data'])
        self.assertIn('ciudad', result['data']['createCiudad'])
        ciudad = result['data']['createCiudad']['ciudad']
        self.assertEqual(ciudad['nombre'], 'Ciudad de prueba')

        # Verificar que se haya creado la ciudad en la base de datos
        self.assertTrue(Ciudad.objects.filter(nombre='Ciudad de prueba').exists())

    def test_delete_ciudad_mutation(self):
        # Crear una ciudad de prueba en la base de datos
        ciudad = Ciudad.objects.create(nombre='Ciudad a eliminar')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                deleteCiudad(id: "%s") {
                    success
                }
            }
        ''' % str(ciudad.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('deleteCiudad', result['data'])
        self.assertTrue(result['data']['deleteCiudad']['success'])

        # Verificar que la ciudad se haya eliminado de la base de datos
        self.assertFalse(Ciudad.objects.filter(id=ciudad.id).exists())

    def test_update_ciudad_mutation(self):
        # Crear una ciudad de prueba en la base de datos
        ciudad = Ciudad.objects.create(nombre='Ciudad inicial')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                updateCiudad(id: "%s", nombre: "Ciudad modificada") {
                    ciudad {
                        id
                        nombre
                    }
                }
            }
        ''' % str(ciudad.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('updateCiudad', result['data'])
        self.assertIn('ciudad', result['data']['updateCiudad'])
        ciudad = result['data']['updateCiudad']['ciudad']
        self.assertEqual(ciudad['nombre'], 'Ciudad modificada')

        # Verificar que la ciudad se haya actualizado en la base de datos
        ciudad_actualizada = Ciudad.objects.get(id=ciudad['id'])
        self.assertEqual(ciudad_actualizada.nombre, 'Ciudad modificada')
