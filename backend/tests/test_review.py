from django.test import TestCase
from app.graphql.schema import schema
from app.models import Ciudad, User, Categoria, Producto, Resena


class ResenaMutationTest(TestCase):

    def test_create_resena_mutation(self):
        # Datos de prueba 
        categoria = Categoria.objects.create(nombre='Categoría de prueba')

        producto = Producto.objects.create(nombre='Producto inicial', categoria=categoria, imagen='productos/inicial.png', stock=1, precio=19.99)

        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            direccion='Dirección de prueba',
            ciudad=ciudad
        )

        # Definir la consulta de mutación para crear una reseña
        mutation = '''
            mutation {
                createResena(input: { usuarioId: %d, productoId: %d, contenido: "Contenido de prueba", calificacion: 4.5 }) {
                    resena {
                        id
                        contenido
                        calificacion
                    }
                }
            }
        ''' % (user.id, producto.id)

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('createResena', result['data'])
        self.assertIn('resena', result['data']['createResena'])
        resena = result['data']['createResena']['resena']
        self.assertEqual(resena['contenido'], 'Contenido de prueba')
        self.assertEqual(resena['calificacion'], 4.5)

        # Verificar que se haya creado la reseña en la base de datos
        self.assertTrue(Resena.objects.filter(contenido='Contenido de prueba').exists())


    def test_update_resena_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Categoría de prueba')
        producto = Producto.objects.create(nombre='Producto inicial', categoria=categoria, imagen='productos/inicial.png', stock=1, precio=19.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            direccion='Dirección de prueba',
            ciudad=ciudad
        )

        # Crear una reseña para el producto
        resena = Resena.objects.create(usuario=user, producto=producto, contenido='Contenido de prueba', calificacion=4.5)

        # Definir la consulta de mutación para actualizar la reseña
        mutation = '''
            mutation {
                updateResena(
                    resenaId: "%s"
                    input: {usuarioId: "%s",
                    productoId: "%s",
                    contenido: "Contenido actualizado",
                    calificacion: 3.5}
                ) {
                    resena {
                    id
                    calificacion
                    contenido
                    }
                }
                }
        ''' % (str(resena.id),str(user.id),str(producto.id))

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('updateResena', result['data'])
        self.assertIn('resena', result['data']['updateResena'])
        resena = result['data']['updateResena']['resena']
        self.assertEqual(resena['contenido'], 'Contenido actualizado')
        self.assertEqual(resena['calificacion'], 3.5)

        # Obtener la reseña actualizada de la base de datos
        resena_db = Resena.objects.get(id=resena['id'])

        # Verificar que la reseña se haya actualizado en la base de datos
        self.assertEqual(resena_db.contenido, 'Contenido actualizado')
        self.assertEqual(resena_db.calificacion, 3.5)
    
    def test_delete_resena_mutation(self):
        # Datos de prueba
        categoria = Categoria.objects.create(nombre='Categoría de prueba')
        producto = Producto.objects.create(nombre='Producto inicial', categoria=categoria, imagen='productos/inicial.png', stock=1, precio=19.99)
        ciudad = Ciudad.objects.create(nombre='Ciudad de prueba')

        user = User.objects.create(
            email='usuario@gmail.com',
            password='contraseña123',
            is_admin=False,
            direccion='Dirección de prueba',
            ciudad=ciudad
        )


        # Crear una reseña para el producto
        resena = Resena.objects.create(usuario=user, producto=producto, contenido='Contenido de prueba', calificacion=4.5)

        # Definir la consulta de mutación para eliminar la reseña
        mutation = '''
            mutation {
                deleteResena(resenaId: %d) {
                    success
                }
            }
        ''' % resena.id

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación de eliminación
        result = response.json()

        # Verificar la respuesta de la mutación de eliminación
        self.assertNotIn('errors', result)
        self.assertIn('data', result)
        self.assertIn('deleteResena', result['data'])
        self.assertTrue(result['data']['deleteResena']['success'])

        # Verificar que la reseña se haya eliminado de la base de datos
        self.assertFalse(Resena.objects.filter(id=resena.id).exists())