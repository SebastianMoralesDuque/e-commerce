from django.test import TestCase
from app.graphql.schema import schema
from app.models import MetodoPago


class MetodoPagoMutationTest(TestCase):
    def test_create_metodo_pago_mutation(self):
        # Definir la consulta de mutación
        mutation = '''
            mutation {
                createMetodoPago(
                    nombre: "Metodo de Pago de prueba"
                ) {
                    metodoPago {
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
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('createMetodoPago', data)
        create_metodo_pago_result = data['createMetodoPago']
        self.assertIsNotNone(create_metodo_pago_result)  # Verificar si create_metodo_pago_result no es None
        if create_metodo_pago_result:
            self.assertIn('metodoPago', create_metodo_pago_result)
            metodo_pago = create_metodo_pago_result['metodoPago']
            self.assertEqual(metodo_pago['nombre'], 'Metodo de Pago de prueba')

            # Verificar que se haya creado el método de pago en la base de datos
            self.assertTrue(MetodoPago.objects.filter(nombre='Metodo de Pago de prueba').exists())

    def test_delete_metodo_pago_mutation(self):
        # Crear un método de pago de prueba en la base de datos
        metodo_pago = MetodoPago.objects.create(nombre='Metodo de Pago de prueba')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                deleteMetodoPago(
                    id: "%s"
                ) {
                    success
                }
            }
        ''' % metodo_pago.id

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('deleteMetodoPago', data)
        delete_metodo_pago_result = data['deleteMetodoPago']
        self.assertIsNotNone(delete_metodo_pago_result)  # Verificar si delete_metodo_pago_result no es None
        if delete_metodo_pago_result:
            self.assertTrue(delete_metodo_pago_result['success'])

            # Verificar que el método de pago se haya eliminado de la base de datos
            self.assertFalse(MetodoPago.objects.filter(id=metodo_pago.id).exists())

    def test_update_metodo_pago_mutation(self):
        # Crear un método de pago de prueba en la base de datos
        metodo_pago = MetodoPago.objects.create(nombre='Metodo de Pago de prueba')

        # Definir la consulta de mutación
        mutation = '''
            mutation {
                updateMetodoPago(
                    id: "%s",
                    nombre: "Metodo de Pago modificado"
                ) {
                    metodoPago {
                        id
                        nombre
                    }
                }
            }
        ''' % metodo_pago.id

        # Ejecutar la mutación utilizando el cliente de pruebas de Django
        response = self.client.post('/graphql/', {
            'query': mutation,
        })

        # Obtener el resultado de la mutación
        result = response.json()

        # Verificar la respuesta de la mutación
        self.assertIn('data', result)
        data = result['data']
        self.assertIn('updateMetodoPago', data)
        update_metodo_pago_result = data['updateMetodoPago']
        self.assertIsNotNone(update_metodo_pago_result)  # Verificar si update_metodo_pago_result no es None
        if update_metodo_pago_result:
            self.assertIn('metodoPago', update_metodo_pago_result)
            metodo_pago = update_metodo_pago_result['metodoPago']
            self.assertEqual(metodo_pago['nombre'], 'Metodo de Pago modificado')

            # Verificar que se haya actualizado el método de pago en la base de datos
            updated_metodo_pago = MetodoPago.objects.get(id=metodo_pago['id'])
            self.assertEqual(updated_metodo_pago.nombre, 'Metodo de Pago modificado')
