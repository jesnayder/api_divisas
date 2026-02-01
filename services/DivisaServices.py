

"""
=============================================================================
SERVICIO DE DIVISAS (CAPA DE LÓGICA DE NEGOCIO)
=============================================================================

Este módulo contiene la clase DivisaService que implementa la lógica de
negocio para obtener información de divisas.

En una arquitectura de capas (Layered Architecture), este servicio actúa
como intermediario entre:
- Controladores (reciben las peticiones HTTP)
- Clientes (se comunican con APIs externas)
- DTOs (definen la estructura de los datos de respuesta)

Responsabilidades de este servicio:
1. Validar la entrada del usuario
2. Coordinar las llamadas al cliente de divisas
3. Transformar los datos crudos de la API en DTOs estructurados
4. Manejar errores de configuración

Patrón: Service Layer (capa de servicios)

Autor: [Jesnayder Pedrozo]
Fecha: Enero 2026
=============================================================================
"""

# httpx: Librería para peticiones HTTP asíncronas
# La usamos para tipar el parámetro http_client
import httpx

# HTTPException: Permite lanzar errores HTTP que FastAPI convierte en respuestas
from fastapi import HTTPException

# DivisaClient: Cliente que se comunica con la API externa de divisas
# Encapsula toda la lógica de comunicación HTTP
from clients.DivisaClient import DivisaClient

# DivisaResponseDTO: Define la estructura de respuesta (Data Transfer Object)
# Usar DTOs garantiza que siempre devolvamos datos con el formato correcto
from DTOs.DivisaDtos import DivisaResponseDTO

# AppSettings: Configuración centralizada de la aplicación
# Contiene URLs, API keys, timeouts, etc.
from appsettings import AppSettings


class DivisaService:
    """
    Servicio principal para obtener información de divisas.
    
    Esta clase implementa el patrón de diseño "Service Layer", que separa
    la lógica de negocio de los controladores y los clientes HTTP.
    
    Ventajas de usar un servicio:
    - Los controladores quedan simples (solo reciben y responden)
    - La lógica de negocio es reutilizable en diferentes contextos
    - Facilita el testing unitario (se puede mockear el cliente)
    - Permite agregar validaciones, caché, logging, etc. en un solo lugar
    - Mejora la mantenibilidad del código
    
    Atributos:
        client (DivisaClient): Instancia del cliente HTTP para la API de divisas
    
    Ejemplo de uso:
        async with httpx.AsyncClient() as http_client:
            service = DivisaService()
            divisa = await service.get_divisa("USD", http_client)
            print(divisa.symbol)  # Imprime: $
    """

    def __init__(self):
        """
        Constructor del servicio.
        
        Inicializa el servicio verificando que la configuración sea correcta
        y creando una instancia del cliente de divisas.
        
        Validaciones realizadas:
        - Verifica que la API key esté configurada
        
        Raises:
            HTTPException(500): Si la API key no está configurada.
                               Esto indica un error de configuración del servidor.
        """
        # =====================================================================
        # VALIDACIÓN CRÍTICA: Verificar que la API key esté configurada
        # =====================================================================
        # Sin la API key, no podemos hacer ninguna petición a freecurrencyapi.com
        # Esta validación se hace en el constructor para fallar rápido
        if not AppSettings.COD_ISO_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="COD_ISO_API_KEY no está configurado. "
                       "Por favor, configura esta variable en el archivo .env"
            )
        
        # =====================================================================
        # INICIALIZAR EL CLIENTE HTTP
        # =====================================================================
        # Creamos una instancia del cliente de divisas
        # Este cliente se reutilizará en todas las llamadas del servicio
        # Encapsula la lógica de comunicación con la API externa
        self.client = DivisaClient()

    async def get_divisa(self, code: str, http_client: httpx.AsyncClient) -> DivisaResponseDTO:
        """
        Obtiene la información de una divisa y la devuelve en formato estructurado.
        
        Este método coordina todo el flujo para obtener los datos de una divisa:
        1. Valida y limpia el código de la divisa (ej: "USD")
        2. Llama al cliente para obtener los datos de la API externa
        3. Transforma los datos en un DTO estructurado y validado
        4. Retorna la respuesta al controlador
        
        Flujo de datos:
            Entrada (code: "USD")
                    ↓
            Limpieza de espacios en blanco
                    ↓
            Cliente HTTP → API externa (freecurrencyapi.com)
                    ↓
            Extracción de campos necesarios
                    ↓
            Empaquetamiento en DTO
                    ↓
            Salida (DivisaResponseDTO)
        
        Args:
            code (str): Código ISO de la divisa a consultar.
                        Ejemplos: "USD", "EUR", "GBP", "JPY"
                        - Puede contener espacios al inicio/final (serán eliminados)
                        - No es sensible a mayúsculas/minúsculas (se normaliza)
            
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
                        Se inyecta desde el controlador para:
                        - Reutilizar conexiones (mejor rendimiento)
                        - Facilitar el testing con mocks
                        - Controlar el ciclo de vida de las conexiones
        
        Returns:
            DivisaResponseDTO: Objeto estructurado con:
                - symbol (str): Símbolo de la divisa (ej: "$" para USD)
                - name (str): Nombre completo (ej: "US Dollar")
                - code (str): Código ISO (ej: "USD")
        
        Raises:
            HTTPException(404): Si la divisa no fue encontrada en la API
            HTTPException(500): Si hay un error con la API de freecurrencyapi.com
        
        Ejemplo de respuesta:
            DivisaResponseDTO(
                symbol="$",
                name="US Dollar",
                code="USD"
            )
        
        Ejemplo de llamada:
            divisa = await service.get_divisa("USD", http_client)
            print(divisa.symbol)  # Imprime: $
        """
        # =====================================================================
        # PASO 1: LIMPIAR Y VALIDAR LA ENTRADA
        # =====================================================================
        # Eliminamos espacios en blanco al inicio y al final del código
        # Esto evita errores si el usuario envía " USD " en lugar de "USD"
        # Ejemplo: " USD  " → "USD"
        code = code.strip()
        
        # Convertimos a mayúsculas para normalizar el código
        # La API espera códigos en mayúsculas (USD, EUR, etc.)
        code = code.upper()

        # =====================================================================
        # PASO 2: OBTENER DATOS DE LA API EXTERNA
        # =====================================================================
        # Llamamos al cliente HTTP para obtener los datos de la divisa
        # El cliente se comunica con freecurrencyapi.com
        # Esto es una operación asíncrona (I/O bound), por eso usamos "await"
        divisa_data = await self.client.get_Divisa(code, http_client)

        # =====================================================================
        # PASO 3: TRANSFORMAR DATOS EN DTO
        # =====================================================================
        # La API retorna MUCHOS campos para cada divisa.
        # Nosotros solo extraemos los campos que necesitamos:
        # - symbol: símbolo de la divisa (ej: "$")
        # - name: nombre completo (ej: "US Dollar")
        # 
        # Empaquetamos estos datos en un DTO (Data Transfer Object)
        # que garantiza:
        # - Validación de tipos automática
        # - Documentación automática en Swagger
        # - Serialización a JSON garantizada
        
        return DivisaResponseDTO(
            symbol=divisa_data["symbol"],
            name=divisa_data["name"],
            code=code
        )
