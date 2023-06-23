from django.test import Client, TestCase
from app.graphql.schema import schema
from app.models import Categoria

class CategoriaMutationTest(TestCase):
    def setUp(self):
        # Configurar los datos de prueba necesarios
        self.client = Client()

    def test_create_categoria_mutation(self):
        # Definir la consulta de mutación
        mutation = '''
            mutation {
                createCategoria(nombre: "Categoria de prueba") {
                    categoria {
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
        self.assertIn('createCategoria', result['data'])
        self.assertIn('categoria', result['data']['createCategoria'])
        categoria = result['data']['createCategoria']['categoria']
        self.assertEqual(categoria['nombre'], 'Categoria de prueba')

        # Verificar que se haya creado la categoría en la base de datos
        self.assertTrue(Categoria.objects.filter(nombre='Categoria de prueba').exists())

    def test_update_categoria_mutation(self):
        # Crear una categoría de prueba en la base de datos
        categoria = Categoria.objects.create(nombre='Categoria inicial')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                updateCategoria(id: "%s", nombre: "Categoria modificada") {
                    categoria {
                        id
                        nombre
                    }
                }
            }
        ''' % str(categoria.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('updateCategoria', result['data'])
        self.assertIn('categoria', result['data']['updateCategoria'])
        categoria = result['data']['updateCategoria']['categoria']
        self.assertEqual(categoria['nombre'], 'Categoria modificada')

        # Verificar que la categoría se haya actualizado en la base de datos
        categoria_actualizada = Categoria.objects.get(id=categoria['id'])
        self.assertEqual(categoria_actualizada.nombre, 'Categoria modificada')

    def test_delete_categoria_mutation(self):
        # Crear una categoría de prueba en la base de datos
        categoria = Categoria.objects.create(nombre='Categoria a eliminar')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                deleteCategoria(id: "%s") {
                    success
                }
            }
        ''' % str(categoria.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('deleteCategoria', result['data'])
        self.assertTrue(result['data']['deleteCategoria']['success'])

        # Verificar que la categoría se haya eliminado de la base de datos
        self.assertFalse(Categoria.objects.filter(id=categoria.id).exists())
