"""
=============================================================================
CONTROLADOR DE DIVISAS (CAPA DE PRESENTACIÓN)
=============================================================================

Este módulo contiene el router de FastAPI que define los endpoints HTTP
para consultar información de divisas. Los controladores son el punto de
entrada de las peticiones HTTP y son responsables de:

1. Recibir las peticiones HTTP del cliente
2. Validar los parámetros de entrada (FastAPI lo hace automáticamente)
3. Llamar al servicio de negocio correspondiente
4. Devolver la respuesta en formato JSON

Patrón utilizado: CONTROLADOR -> SERVICIO -> CLIENTE -> API EXTERNA

Ejemplo de uso:
    GET /api/divisas/USD
    
    Retorna:
    {
        "symbol": "$",
        "name": "US Dollar",
        "code": "USD"
    }

Autor: [jesnayder pedrozo]
Fecha: Enero 2026
=============================================================================
"""

# httpx: Librería moderna para hacer peticiones HTTP asíncronas
import httpx

# APIRouter: Permite organizar los endpoints en módulos separados
from fastapi import APIRouter

# DivisaService: Contiene la lógica de negocio para obtener divisas
from services.DivisaServices import DivisaService

# DivisaResponseDTO: Define la estructura de la respuesta (validación automática)
from DTOs.DivisaDtos import DivisaResponseDTO

# =============================================================================
# CONFIGURACIÓN DEL ROUTER
# =============================================================================
# Creamos un router con prefijo "/api" para todas las rutas
# Esto significa que todas las rutas estarán bajo /api/...
router = APIRouter(prefix="/api")

# =============================================================================
# ENDPOINT: GET /api/divisas/{code}
# =============================================================================
@router.get(
    "/divisas/{code}",  # Ruta: /api/divisas/USD
    response_model=DivisaResponseDTO,  # Validación y documentación automática
    summary="Obtener información de una divisa",  # Título en Swagger
    description="Retorna los datos (símbolo, nombre, código) de una divisa específica",
    tags=["Divisas"]  # Categoría en la documentación
)
async def getdivisas(code: str):
    """
    Endpoint para obtener información de una divisa.
    
    Este endpoint:
    1. Recibe el código de la divisa (ej: "USD", "EUR")
    2. Crea un cliente HTTP asíncrono
    3. Inicializa el servicio de divisas
    4. Solicita los datos al servicio
    5. Retorna la respuesta en formato JSON
    
    Args:
        code (str): Código ISO de la divisa (ej: "USD", "EUR", "GBP")
    
    Returns:
        DivisaResponseDTO: Objeto con estructura:
            {
                "symbol": "$",
                "name": "US Dollar",
                "code": "USD"
            }
    
    Raises:
        HTTPException(404): Si la divisa no existe
        HTTPException(500): Si hay error en la API externa
    
    Ejemplo de llamada:
        curl http://localhost:8000/api/divisas/USD
    """
    
    # Creamos un cliente HTTP asíncrono (context manager)
    # El "async with" garantiza que la conexión se cierre correctamente
    async with httpx.AsyncClient() as http_client:
        
        # Inicializamos el servicio de divisas
        # El servicio contiene la lógica de negocio
        divisa_service = DivisaService()
        
        # Llamamos al método del servicio para obtener los datos de la divisa
        # Usamos "await" porque es una operación asíncrona (I/O bound)
        divisa_response = await divisa_service.get_divisa(code, http_client)
        
        # Retornamos la respuesta (FastAPI automáticamente la serializa a JSON)
        # Pydantic valida que coincida con DivisaResponseDTO
        return divisa_response
