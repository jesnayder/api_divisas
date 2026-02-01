"""
=============================================================================
DTOs (DATA TRANSFER OBJECTS) - MODELOS DE DATOS
=============================================================================

Este módulo contiene los DTOs (Data Transfer Objects) utilizados para
estructurar los datos de respuesta de la API.

¿Qué es un DTO?
---------------
Un DTO es un objeto que define la estructura de los datos que se transfieren
entre capas de la aplicación o hacia/desde clientes externos.

Un DTO NO contiene lógica de negocio, solo estructura y validación.

¿Por qué usar DTOs en FastAPI?
------------------------------
1. VALIDACIÓN AUTOMÁTICA: Pydantic valida que los datos cumplan el esquema
2. DOCUMENTACIÓN: FastAPI genera docs automáticos (Swagger) basados en los DTOs
3. SERIALIZACIÓN: Convierte automáticamente objetos Python a JSON
4. TYPE HINTS: Mejora el autocompletado y detección de errores en el IDE
5. CONSISTENCIA: Garantiza que todas las respuestas tengan el mismo formato
6. SEGURIDAD: Solo expone los campos que queremos, oculta campos internos

Ejemplo de respuesta JSON generada:
{
    "symbol": "$",
    "name": "US Dollar",
    "code": "USD"
}

Ventajas de usar DTOs:
- Si cambia la estructura de la API interna, el cliente no se ve afectado
- Podemos validar datos antes de usarlos
- La documentación automática siempre es correcta
- El equipo sabe exactamente qué campos retorna cada endpoint

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# BaseModel: Clase base de Pydantic para definir modelos de datos
# Proporciona:
# - Validación automática de tipos
# - Serialización a JSON
# - Generación automática de documentación
from pydantic import BaseModel, Field


class DivisaResponseDTO(BaseModel):
    """
    DTO para la respuesta de información de una divisa.
    
    Este modelo define la estructura exacta de los datos que se devuelven
    cuando un cliente consulta la información de una divisa específica.
    
    Características:
    - Todos los campos son obligatorios (no tienen valor por defecto)
    - FastAPI valida automáticamente que los datos cumplan este esquema
    - Se genera documentación automática en Swagger UI
    - Pydantic convierte automáticamente a JSON
    
    Patrón: Data Transfer Object (DTO)
    - Encapsula los datos de una respuesta
    - No contiene lógica de negocio
    - Facilita validación y documentación
    
    Atributos:
        symbol (str): Símbolo de la divisa (ej: "$" para USD, "€" para EUR)
        name (str): Nombre completo de la divisa (ej: "US Dollar")
        code (str): Código ISO de la divisa (ej: "USD", "EUR", "GBP")
    
    Ejemplo de uso en el código:
        >>> divisa = DivisaResponseDTO(
        ...     symbol="$",
        ...     name="US Dollar",
        ...     code="USD"
        ... )
        >>> divisa.model_dump()  # Convierte a diccionario
        {'symbol': '$', 'name': 'US Dollar', 'code': 'USD'}
        
        >>> divisa.model_dump_json()  # Convierte a JSON string
        '{\"symbol\": \"$\", \"name\": \"US Dollar\", \"code\": \"USD\"}'
    
    Ejemplo de respuesta HTTP:
        GET /api/divisas/USD
        
        Respuesta (status 200):
        {
            "symbol": "$",
            "name": "US Dollar",
            "code": "USD"
        }
    """

    # =========================================================================
    # CAMPO: symbol (símbolo de la divisa)
    # =========================================================================
    # Field(...) indica que el campo es OBLIGATORIO
    # El primer parámetro (...) es un marcador especial que significa "required"
    # Si un campo tiene valor por defecto, no es obligatorio
    
    symbol: str = Field(
        ...,  # ... = campo requerido (no tiene valor por defecto)
        description="Símbolo de la divisa usado en transacciones",
        examples=["$", "€", "£", "¥", "₹"]  # Ejemplos para la documentación
    )
    
    # =========================================================================
    # CAMPO: name (nombre de la divisa)
    # =========================================================================
    # Campo tipo string con descripción y ejemplos
    
    name: str = Field(
        ...,  # Campo obligatorio
        description="Nombre completo de la divisa en inglés",
        examples=["US Dollar", "Euro", "British Pound", "Japanese Yen", "Indian Rupee"]
    )
    
    # =========================================================================
    # CAMPO: code (código ISO de la divisa)
    # =========================================================================
    # Campo tipo string que contiene el código ISO de 3 letras
    
    code: str = Field(
        ...,  # Campo obligatorio
        description="Código ISO 4217 de la divisa (3 letras)",
        examples=["USD", "EUR", "GBP", "JPY", "INR", "MXN"]
    )

    # =========================================================================
    # CONFIGURACIÓN DEL MODELO (PYDANTIC CONFIG)
    # =========================================================================
    class Config:
        """
        Configuración adicional del modelo Pydantic.
        
        Parámetros disponibles:
        - json_schema_extra: Agrega información extra al esquema JSON
        - validate_assignment: Valida cambios después de la creación
        - str_strip_whitespace: Elimina espacios en blanco automáticamente
        - etc.
        """
        # json_schema_extra: Proporciona ejemplos completos que aparecen
        # en la documentación de Swagger UI y en /docs
        # Esto ayuda a los desarrolladores a entender exactamente
        # qué estructura esperar
        json_schema_extra = {
            "example": {
                "symbol": "$",
                "name": "US Dollar",
                "code": "USD"
            }
        }
