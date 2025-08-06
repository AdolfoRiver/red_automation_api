# test_gestion_dispositivos.py

import unittest
from unittest.mock import patch, MagicMock
from gestion_dispositivos import DeviceManager

class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        """Configuración que se ejecuta antes de cada prueba."""
        self.manager = DeviceManager()

    @patch('requests.get')
    def test_listar_dispositivos_exito(self, mock_get):
        """Prueba que la lista de dispositivos se maneja correctamente con una respuesta 200 OK."""
        print("\nEjecutando: test_listar_dispositivos_exito")
        # Simular una respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1, "first_name": "George"}]}
        mock_get.return_value = mock_response

        # Llamar al método que estamos probando
        resultado = self.manager.listar_dispositivos()

        # Verificar que el resultado es el esperado
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["data"][0]["first_name"], "George")
        # Verificar que requests.get fue llamado con la URL correcta
        mock_get.assert_called_with("https://reqres.in/api/users", params={"page": 1})

    @patch('requests.post')
    def test_agregar_dispositivo_exito(self, mock_post):
        """Prueba que se puede agregar un dispositivo con una respuesta 201 Created."""
        print("Ejecutando: test_agregar_dispositivo_exito")
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"name": "Router-A", "job": "Core", "id": "123", "createdAt": "2025-01-01"}
        mock_post.return_value = mock_response

        resultado = self.manager.agregar_dispositivo(nombre="Router-A", trabajo="Core")
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["name"], "Router-A")
        self.assertIn("id", resultado)

    @patch('requests.delete')
    def test_eliminar_dispositivo_exito(self, mock_delete):
        """Prueba la eliminación exitosa de un dispositivo con una respuesta 204 No Content."""
        print("Ejecutando: test_eliminar_dispositivo_exito")
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        resultado = self.manager.eliminar_dispositivo(user_id=5)
        
        self.assertIsNone(resultado) # Una respuesta 204 no devuelve cuerpo

    @patch('requests.get')
    def test_dispositivo_no_encontrado_404(self, mock_get):
        """Prueba el manejo de un error 404 Not Found."""
        print("Ejecutando: test_dispositivo_no_encontrado_404")
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Probamos con el método de actualizar, pero podría ser cualquiera que use un ID
        resultado = self.manager.actualizar_dispositivo(user_id=999, nombre="Fantasma", trabajo="Inexistente")
        
        self.assertIsNone(resultado) # Nuestro manejador de errores devuelve None para los errores

if __name__ == '__main__':
    unittest.main(verbosity=2)
