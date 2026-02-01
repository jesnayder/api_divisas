"""
=============================================================================
CONFIGURACIÓN CENTRALIZADA DE LA APLICACIÓN
=============================================================================

Este módulo contiene la configuración global de la aplicación, cargando
las variables de entorno desde el archivo .env y exponiendo constantes
de configuración.

¿Por qué usar un archivo de configuración centralizado?
-------------------------------------------------------
1. SEGURIDAD: Las API keys y secretos NO se guardan en el código fuente
2. FLEXIBILIDAD: Cambios de configuración sin modificar código
3. AMBIENTES: Diferentes configuraciones para desarrollo, staging, producción
4. MANTENIBILIDAD: Un solo lugar para gestionar todas las configuraciones
5. BUENAS PRÁCTICAS: Sigue el patrón de factorización de configuración


Autor: [Jesnayder Pedrozo]
Fecha: Enero 2026
=============================================================================
"""

# os: Módulo para interactuar con el sistema operativo
# Usamos os.getenv() para leer variables de entorno
import os

# python-dotenv: Librería para cargar variables de un archivo .env
# Esto es muy útil en desarrollo para no configurar variables del sistema
# Librería: pip install python-dotenv
from dotenv import load_dotenv


# =============================================================================
# CARGAR VARIABLES DE ENTORNO
# =============================================================================
# load_dotenv() busca un archivo llamado .env en el directorio actual
# y carga todas las variables definidas en él como variables de entorno
# 
# Ejemplo de contenido de .env:
# COD_ISO_API_KEY=abc123
# DATA_DIVISAS_URL=https://api.example.com
# 
# Después de load_dotenv(), puedes acceder con os.getenv("COD_ISO_API_KEY")
# 
# Si la variable no existe, os.getenv() devuelve None (si no especificas default)
# Ejemplo: os.getenv("VARIABLE_NO_EXISTE", "valor_por_defecto")
load_dotenv()


class AppSettings:
    """
    Clase de configuración que contiene todas las constantes de la aplicación.
    
    Usamos una clase en lugar de variables sueltas por:
    - Agrupa todas las configuraciones en un solo lugar
    - Permite validación y transformación de valores
    - Facilita el autocompletado en el IDE
    - Es más fácil de mockear en tests
    - Sigue el patrón Singleton (una sola instancia de configuración)
    
    Uso:
        from appsettings import AppSettings
        
        api_key = AppSettings.COD_ISO_API_KEY
        url = AppSettings.DATA_DIVISAS_URL
        timeout = AppSettings.TIMEOUT_SECONDS
    
    Nota importante: Todos los atributos son de clase (class attributes)
    Esto significa que NO necesitas crear una instancia para usarlos:
        AppSettings.COD_ISO_API_KEY  # ✓ Correcto
        AppSettings().COD_ISO_API_KEY  # También funciona, pero innecesario
        
    Ventajas de atributos de clase:
    - Se cargan solo una vez cuando se importa el módulo
    - No hay overhead de crear instancias
    - Ideal para valores estáticos
    """

    # =========================================================================
    # CONFIGURACIÓN DE LA API DE DIVISAS (FREECURRENCYAPI.COM)
    # =========================================================================
    
    # COD_ISO_API_KEY: API Key de freecurrencyapi.com (REQUERIDA)
    # 
    # Cómo obtenerla:
    # 1. Ir a https://freecurrencyapi.com
    # 2. Registrarse (gratis)
    # 3. Copiar la API key desde el dashboard
    # 
    # ⚠️ SEGURIDAD: Esta key debe mantenerse PRIVADA y NUNCA subirse a repositorios públicos
    # Siempre configúrala en el archivo .env (que está en .gitignore)
    #
    # Ejemplo de valor: "fca_live_lfffgggggghhhhhjjuyyyyyyyyygbbbgubyu"
    # Tipo: string
    COD_ISO_API_KEY = os.getenv("COD_ISO_API_KEY")
    
    # DATA_DIVISAS_URL: URL de la API de divisas
    # 
    # Esta es la URL base del endpoint que proporciona datos de divisas
    # Documentación oficial: https://freecurrencyapi.com/docs
    #
    # Ejemplo de URL: https://api.freecurrencyapi.com/v1/currencies
    # Método HTTP: GET
    # Parámetros requeridos:
    #   - currencies: código de la divisa (USD, EUR, GBP, etc.)
    #   - apikey: tu API key para autenticación
    #
    # Ejemplo de petición:
    # GET https://api.freecurrencyapi.com/v1/currencies?currencies=USD&apikey=tu_key
    #
    # Tipo: string (URL completa)
    DATA_DIVISAS_URL = os.getenv("DATA_DIVISAS_URL")
    
    # =========================================================================
    # CONFIGURACIÓN DE TIMEOUTS
    # =========================================================================
    
    # TIMEOUT_SECONDS: Tiempo máximo de espera para las peticiones HTTP
    #
    # ¿Para qué sirve?
    # - Evita que la aplicación se quede esperando indefinidamente
    # - Si la API no responde en 5 segundos, se cancela la petición
    # - Previene bloqueos innecesarios
    #
    # Valor: 5 segundos (es un buen balance entre rapidez y fiabilidad)
    # - Si es muy bajo (ej: 1s), fallarán peticiones legítimas
    # - Si es muy alto (ej: 30s), el usuario esperará demasiado
    #
    # Tipo: entero (segundos)
    TIMEOUT_SECONDS = 5

    # =========================================================================
    # MÉTODOS ÚTILES (Opcional)
    # =========================================================================
    
    @staticmethod
    def validate():
        """
        Valida que todas las configuraciones requeridas estén presentes.
        
        Útil para validar al startup que no falta ninguna variable.
        Puede llamarse en main.py al iniciar la aplicación.
        
        Ejemplo:
            app = FastAPI()
            AppSettings.validate()  # Lanza excepción si falta algo
        """
        if not AppSettings.COD_ISO_API_KEY:
            raise ValueError("COD_ISO_API_KEY no está configurada en .env")
        
        if not AppSettings.DATA_DIVISAS_URL:
            raise ValueError("DATA_DIVISAS_URL no está configurada en .env")
    
    @staticmethod
    def get_summary():
        """
        Retorna un resumen de la configuración (útil para debugging).
        
        No muestra valores sensibles (API keys).
        
        Retorna:
            dict: Resumen de configuración
        """
        return {
            "api_configured": bool(AppSettings.COD_ISO_API_KEY),
            "url_configured": bool(AppSettings.DATA_DIVISAS_URL),
            "timeout": AppSettings.TIMEOUT_SECONDS,
            "url": AppSettings.DATA_DIVISAS_URL
        }
