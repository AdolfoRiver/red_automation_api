# gestion_dispositivos.py

import requests
import json

class DeviceManager:
    """
    Clase para gestionar dispositivos de red a través de una API REST.
    Utiliza la API de reqres.in para simular las operaciones.
    """
    def __init__(self, base_url="https://reqres.in/api"):
        """Inicializa el gestor con la URL base de la API."""
        self.base_url = base_url

    def _handle_response(self, response):
        """Función auxiliar para manejar las respuestas HTTP y los errores."""
        status_code = response.status_code
        
        # Códigos de éxito
        if status_code == 200: # OK
            print(f"Éxito (200 OK): La solicitud se completó correctamente.")
            return response.json()
        elif status_code == 201: # Created
            print(f"Éxito (201 Created): El recurso fue creado correctamente.")
            return response.json()
        elif status_code == 204: # No Content
            print(f"Éxito (204 No Content): El recurso fue eliminado y no hay contenido que devolver.")
            return None # No hay JSON en una respuesta 204
        
        # Códigos de error del cliente
        elif status_code == 400: # Bad Request
            print("Error (400 Bad Request): La solicitud es incorrecta o mal formada.")
        elif status_code == 401: # Unauthorized
            print("Error (401 Unauthorized): No tienes autenticación para realizar esta acción.")
        elif status_code == 404: # Not Found
            print("Error (404 Not Found): El recurso solicitado no fue encontrado.")
        
        # Código de error del servidor
        elif status_code >= 500: # Server Error
            print(f"Error del Servidor ({status_code}): Ocurrió un problema en el servidor.")
        
        else: # Otros códigos
            print(f"Error inesperado. Código de estado: {status_code}")
            
        return None

    def agregar_dispositivo(self, nombre, trabajo):
        """Agrega un nuevo dispositivo (usuario simulado)."""
        print("\n--- INTENTANDO AGREGAR DISPOSITIVO ---")
        endpoint = f"{self.base_url}/users"
        payload = {"name": nombre, "job": trabajo}
        try:
            response = requests.post(endpoint, json=payload)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    def listar_dispositivos(self, pagina=1):
        """Obtiene la lista de dispositivos (usuarios simulados)."""
        print("\n--- INTENTANDO LISTAR DISPOSITIVOS ---")
        endpoint = f"{self.base_url}/users"
        params = {"page": pagina}
        try:
            response = requests.get(endpoint, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    def actualizar_dispositivo(self, user_id, nombre, trabajo):
        """Actualiza la información de un dispositivo existente."""
        print(f"\n--- INTENTANDO ACTUALIZAR DISPOSITIVO ID: {user_id} ---")
        endpoint = f"{self.base_url}/users/{user_id}"
        payload = {"name": nombre, "job": trabajo}
        try:
            response = requests.put(endpoint, json=payload)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    def eliminar_dispositivo(self, user_id):
        """Elimina un dispositivo."""
        print(f"\n--- INTENTANDO ELIMINAR DISPOSITIVO ID: {user_id} ---")
        endpoint = f"{self.base_url}/users/{user_id}"
        try:
            response = requests.delete(endpoint)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

# --- Bloque de ejecución principal para probar el script ---
if __name__ == "__main__":
    manager = DeviceManager()

    # 1. Agregar un dispositivo
    nuevo_dispositivo = manager.agregar_dispositivo(nombre="Router-Principal", trabajo="Core-Gateway")
    if nuevo_dispositivo:
        print("Respuesta JSON:", json.dumps(nuevo_dispositivo, indent=4))
        # Guardamos el ID que nos devuelve la API para usarlo después
        nuevo_id = nuevo_dispositivo.get("id")

    # 2. Listar dispositivos
    lista = manager.listar_dispositivos(pagina=2)
    if lista:
        print("Respuesta JSON:", json.dumps(lista, indent=4))

    # 3. Actualizar el dispositivo que acabamos de crear (usamos un ID fijo para el ejemplo)
    dispositivo_actualizado = manager.actualizar_dispositivo(user_id=2, nombre="Switch-Acceso-01", trabajo="Capa 2")
    if dispositivo_actualizado:
        print("Respuesta JSON:", json.dumps(dispositivo_actualizado, indent=4))

    # 4. Eliminar un dispositivo
    manager.eliminar_dispositivo(user_id=2)

    # 5. Probar un error 404 (ID que no existe)
    print("\n--- PROBANDO UN ERROR 404 ---")
    manager.listar_dispositivos(pagina=999)
