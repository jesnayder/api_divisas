# httpx es una librería moderna para hacer peticiones HTTP asíncronas en Python
# Es similar a 'requests' pero soporta async/await de forma nativa
import httpx

# HTTPException nos permite lanzar errores HTTP con códigos de estado específicos
# FastAPI los convierte automáticamente en respuestas HTTP apropiadas
from fastapi import HTTPException

# Importamos la configuración centralizada de la aplicación
# Contiene las URLs de la API, la API key y otros parámetros
from appsettings import AppSettings


class DivisaClient:
    def __init__(self):
        """
        Constructor de la clase.
        
        Actualmente no requiere inicialización especial, pero se mantiene
        por si en el futuro se necesita inyectar dependencias o configuración.
        """
        pass

    async def get_Divisa(self, code: str, http_client: httpx.AsyncClient) -> dict:
        """
        Obtiene los datos de la divisa desde freecurrencyapi.com.
        
        Args:
            cod (str): Código de la divisa a buscar (ej: "USD", "EUR")
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
        
        Returns:
            dict: Diccionario con los datos de la divisa
        
        Raises:
            HTTPException(404): Si la divisa no fue encontrada
            HTTPException(500): Si hay un error en la API
        """
        # Realizamos la petición GET a la API de Divisas con parámetro currencies
        response = await http_client.get(
            AppSettings.DATA_DIVISAS_URL,
            params={
                "currencies": code,
                "apikey": AppSettings.COD_ISO_API_KEY
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        # =====================================================================
        # VALIDACIÓN 1: Verificar códigos de error HTTP específicos
        # =====================================================================
        # Si es 404 o 422, probablemente la divisa no existe o código inválido
        if response.status_code == 422 or response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Divisa '{code}' no encontrada. Verifica que el código ISO sea válido. error code: {response.reason_phrase}"
            )
        
        # Si es cualquier otro error (500, 401, 403, etc.), error de servidor
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error en la API externa (código {response.status_code}): {response.reason_phrase}"
            )

        # =====================================================================
        # VALIDACIÓN 2: Convertir respuesta JSON y verificar estructura
        # =====================================================================
        # Convertimos la respuesta JSON a un diccionario
        data = response.json()
        # =====================================================================
        # ÉXITO: Retornar los datos de la divisa solicitada
        # =====================================================================
        return data["data"][code]