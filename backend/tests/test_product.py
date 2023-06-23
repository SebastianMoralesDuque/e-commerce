from django.test import TestCase
from graphene.test import Client
from app.graphql.schema import schema
from app.models import Categoria
from app.models import Producto


class ProductoMutationTest(TestCase):
    def setUp(self):
        # Configurar los datos de prueba necesarios
        self.client = Client(schema)

    def test_create_producto_mutation(self):
        # Crear una categoría de prueba en la base de datos
        categoria = Categoria.objects.create(nombre='Categoría de prueba')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                createProducto(nombre: "Producto de prueba", categoriaId: %d, imagen: "productos/prueba.png", stock: 1) {
                    producto {
                        id
                        nombre
                    }
                }
            }
        ''' % categoria.id

        # Ejecutar la mutación utilizando el cliente de pruebas de GraphQL
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', executed)
        self.assertIn('createProducto', executed['data'])
        self.assertIn('producto', executed['data']['createProducto'])
        producto = executed['data']['createProducto']['producto']
        self.assertEqual(producto['nombre'], 'Producto de prueba')

        # Verificar que se haya creado el producto en la base de datos
        self.assertTrue(Producto.objects.filter(nombre='Producto de prueba').exists())

        # Obtener el producto de la base de datos
        producto_db = Producto.objects.get(nombre='Producto de prueba')

        # Realizar una prueba de eliminación de producto
        mutation = '''
            mutation {
                deleteProducto(id: %d) {
                    success
                }
            }
        ''' % producto_db.id

        # Ejecutar la mutación para eliminar el producto
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación de eliminación
        self.assertNotIn('errors', executed)
        self.assertIn('deleteProducto', executed['data'])
        self.assertTrue(executed['data']['deleteProducto']['success'])

    def test_update_producto_mutation(self):
        # Crear una categoría de prueba en la base de datos
        categoria = Categoria.objects.create(nombre='Categoría de prueba')

        # Crear un producto de prueba en la base de datos
        producto = Producto.objects.create(nombre='Producto inicial', categoria=categoria, imagen='productos/inicial.png', stock=1)

        # Definir la consulta de mutación para actualizar el producto
        mutation = '''
            mutation {
                updateProducto(id: %d, nombre: "Producto actualizado", imagen: "productos/actualizado.png") {
                    producto {
                        id
                        nombre
                        imagen
                    }
                }
            }
        ''' % producto.id

        # Ejecutar la mutación utilizando el cliente de pruebas de GraphQL
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', executed)
        self.assertIn('updateProducto', executed['data'])
        self.assertIn('producto', executed['data']['updateProducto'])
        producto = executed['data']['updateProducto']['producto']
        self.assertEqual(producto['nombre'], 'Producto actualizado')
        self.assertEqual(producto['imagen'], 'productos/actualizado.png')

        # Obtener el producto actualizado de la base de datos
        producto_db = Producto.objects.get(id=producto['id'])

        # Verificar que los campos se hayan actualizado correctamente en la base de datos
        self.assertEqual(producto_db.nombre, 'Producto actualizado')
        self.assertEqual(producto_db.imagen, 'productos/actualizado.png')

        # Realizar una prueba de eliminación de producto
        mutation = '''
            mutation {
                deleteProducto(id: %d) {
                    success
                }
            }
        ''' % producto_db.id

        # Ejecutar la mutación para eliminar el producto
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación de eliminación
        self.assertNotIn('errors', executed)
        self.assertIn('deleteProducto', executed['data'])
        self.assertTrue(executed['data']['deleteProducto']['success'])


    def test_delete_producto_mutation(self):
        # Crear una categoría de prueba en la base de datos
        categoria = Categoria.objects.create(nombre='Categoría de prueba')

        # Crear un producto de prueba en la base de datos
        producto = Producto.objects.create(nombre='Producto de prueba', categoria=categoria, imagen='productos/prueba.png', stock=1)

        # Definir la consulta de mutación para eliminar el producto
        mutation = '''
            mutation {
                deleteProducto(id: %d) {
                    success
                }
            }
        ''' % producto.id

        # Ejecutar la mutación utilizando el cliente de pruebas de GraphQL
        executed = self.client.execute(mutation)

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', executed)
        self.assertIn('deleteProducto', executed['data'])
        self.assertTrue(executed['data']['deleteProducto']['success'])

        # Verificar que el producto se haya eliminado de la base de datos
        self.assertFalse(Producto.objects.filter(id=producto.id).exists())