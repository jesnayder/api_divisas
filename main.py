"""
=============================================================================
PUNTO DE ENTRADA DE LA APLICACIÓN FASTAPI
=============================================================================

Este es el archivo principal de la aplicación. Aquí se configura e inicializa
la instancia de FastAPI y se registran todos los routers (controladores).

¿Qué es FastAPI?
----------------
FastAPI es un framework moderno y de alto rendimiento para construir APIs
con Python 3.7+ basado en estándares como OpenAPI y JSON Schema.

Características principales de FastAPI:
- Rápido: Rendimiento similar a NodeJS y Go (gracias a Starlette y Pydantic)
- Fácil: Diseñado para ser intuitivo y fácil de aprender
- Robusto: Código listo para producción (validación automática)
- Documentado: Genera docs automáticos (Swagger UI y ReDoc)
- Inteligente: Autocompletado en el IDE gracias a type hints

Arquitectura de la aplicación:
    [Cliente HTTP] → FastAPI → Router → Controlador → Servicio → Cliente HTTP → API Externa

Para ejecutar la aplicación:
    # En desarrollo (con reinicio automático):
    uvicorn main:app --reload
    
    # En producción:
    uvicorn main:app --host 0.0.0.0 --port 8000

Documentación automática disponible en:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    - OpenAPI JSON: http://localhost:8000/openapi.json

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================

# FastAPI: El framework principal para crear la API
# Importamos la clase FastAPI que será el núcleo de nuestra aplicación
# FastAPI es una clase que representa toda nuestra aplicación web
from fastapi import FastAPI

# Router: Importamos el router del controlador de divisas
# Los routers permiten organizar los endpoints en módulos separados
# Esto mantiene el código limpio y modular
from controllers.DivisasController import router as divisas_router


# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================
# Creamos la instancia principal de FastAPI
# Esta instancia es el punto central que maneja todas las peticiones HTTP
# 
# Parámetros:
# - title: Título que aparece en la documentación (Swagger UI)
# - description: Descripción de la API (también en Swagger)
# - version: Versión de la API (útil para control de cambios)
# - contact: Información de contacto del desarrollador
# - license_info: Información sobre la licencia
app = FastAPI(
    title="DIVISAS API",  # Título que aparece en /docs
    description="""
    ## API DE CONSULTA DE DIVISAS 💱
    
    Esta API permite consultar información sobre diferentes divisas (monedas)
    del mundo, incluyendo:
    - Símbolo de la divisa (ej: $, €, £)
    - Nombre completo (ej: US Dollar, Euro)
    - Código ISO (ej: USD, EUR, GBP)
    
    ### Funcionalidades:
    * Obtener información completa de una divisa
    * Búsqueda por código ISO
    * Respuestas en formato JSON estructurado
    
    ### Tecnologías utilizadas:
    * FastAPI - Framework web moderno
    * httpx - Cliente HTTP asíncrono
    * Pydantic - Validación de datos
    * freecurrencyapi.com - Datos de divisas
    
    ### Ejemplo de uso:
    ```bash
    curl http://localhost:8000/api/divisas/USD
    ```
    """,
    version="1.0.0",  # Versión de la API (sigue semántica: major.minor.patch)
    contact={
        "name": "Jesnayder Pedrozo",
        "url": "https://ejemplo.com",
        "email": "jesph08@email.com"
    },
    license_info={
        "name": "Ing. Jesnayder Pedrozo",
        "url": "https://opensource.org/licenses/MIT"
    }
)


# =============================================================================
# ENDPOINT RAÍZ (HOME) - HEALTH CHECK
# =============================================================================
# Este endpoint se usa típicamente para:
# - Verificar que la API está corriendo
# - Health checks (monitoreo)
# - Pruebas de conectividad
@app.get(
    "/",  # Ruta raíz del servidor
    summary="Página de inicio",  # Título corto en Swagger
    description="Endpoint de bienvenida que confirma que la API está funcionando",
    tags=["General"]  # Categoría en la documentación
)
def home():
    """
    Endpoint de bienvenida / Health Check.
    
    Este endpoint sirve como verificación de que la API está funcionando
    correctamente. Es útil para:
    - Health checks en sistemas de monitoreo
    - Verificar conectividad desde clientes
    - Pruebas rápidas de disponibilidad
    
    Returns:
        dict: Mensaje de bienvenida con información de la API
        
    Ejemplo de respuesta (HTTP 200):
        {
            "message": "Welcome to the Weather API",
            "docs": "Visita /docs para ver la documentación interactiva",
            "version": "1.0.0"
        }
    
    HTTP Status Codes:
        200: OK - La API está corriendo correctamente
    """
    return {
        "message": "Welcome to Divisas API",
        "docs": "Visita /docs para ver la documentación interactiva",
        "redoc": "Visita /redoc para ver la documentación en ReDoc",
        "version": "1.0.0"
    }


# =============================================================================
# REGISTRO DE ROUTERS (CONTROLLERS)
# =============================================================================
# Los routers agrupan endpoints relacionados en módulos separados
# 
# ¿Por qué usar routers?
# - Mantiene el código organizado y modular
# - Facilita el mantenimiento (cambios en un lugar)
# - Permite agregar middlewares específicos por grupo de rutas
# - Mejora la legibilidad del código
#
# Router incluido: divisas_router
# - Contiene todos los endpoints relacionados con divisas
# - Incluye el prefijo "/api" (configurado en DivisasController)
# 
# Rutas disponibles después de este registro:
# - GET /api/divisas/{code} - Obtener información de una divisa

app.include_router(divisas_router)


# =============================================================================
# PUNTO DE ENTRADA: EJECUCIÓN DE LA APLICACIÓN
# =============================================================================
# Este bloque solo se ejecuta si corremos el archivo directamente
# Si importamos este módulo desde otro lugar, este código NO se ejecuta
# 
# Ejemplo:
# - Si ejecutas: python main.py → Sí se ejecuta
# - Si importas: from main import app → No se ejecuta
if __name__ == "__main__":
    # Importamos uvicorn (el servidor ASGI que ejecuta FastAPI)
    # uvicorn es el servidor recomendado para FastAPI
    import uvicorn
    
    # =====================================================================
    # CONFIGURACIÓN DEL SERVIDOR DE DESARROLLO
    # =====================================================================
    # uvicorn.run() inicia el servidor web
    # 
    # Parámetros principales:
    # - "main:app": Ruta al objeto app (archivo:variable)
    # - host: Dirección IP donde escuchar
    # - port: Puerto del servidor
    # - reload: Reiniciar automáticamente en caso de cambios
    # - log_level: Nivel de detalle de logs
    
    uvicorn.run(
        "main:app",  # Ruta al objeto app (archivo:variable)
        host="127.0.0.1",  # Solo accesible localmente (para desarrollo)
                           # Usa "0.0.0.0" en producción si quieres acceso remoto
        port=8000,  # Puerto del servidor (1-65535)
                    # Puertos comunes: 8000 (desarrollo), 80 (HTTP), 443 (HTTPS)
        reload=True  # Reinicio automático cuando hay cambios en el código
                     # Solo para desarrollo, desactivar en producción
    )

# ============================================================================
# NOTA: EJECUCIÓN EN PRODUCCIÓN
# ============================================================================
# Para producción, NO uses uvicorn.run() ni reload=True
# 
# Usa Gunicorn con Uvicorn workers:
# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
#
# Alternativas:
# - Daphne (para WebSockets)
# - Hypercorn (alternativa a Uvicorn)
# - Docker + Kubernetes
