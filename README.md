# Api Divisas

API RESTful para consultar información de divisas usando FastAPI.

**Breve descripción**: Esta API permite consultar datos básicos de una divisa
(símbolo, nombre y código) a partir de su código ISO. Actúa como una
capa que solicita información a la API externa `freecurrencyapi.com` y
expone respuestas limpias y validadas mediante FastAPI y Pydantic.

---

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso Rápido](#uso-rápido)
5. [Endpoints](#endpoints)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [Arquitectura](#arquitectura)
8. [Códigos de Error HTTP](#códigos-de-error-http)
9. [Códigos ISO de Divisas](#códigos-iso-de-divisas)
10. [Tecnologías Utilizadas](#tecnologías-utilizadas)
11. [Soporte](#soporte)
12. [Autor](#autor)

---

## Requisitos

- Python 3.8+
- API Key de freecurrencyapi.com

---

## Instalación

```bash
git clone https://github.com/jesnayder/api_divisas.git
cd api_divisas
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Configuración

### 1. Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con tu API Key:

```env
COD_ISO_API_KEY=tu_api_key_aqui
DATA_DIVISAS_URL=https://api.freecurrencyapi.com/v1/currencies
```

### 2. Iniciar la API

```bash
uvicorn main:app --reload
```

**Acceso**:
- API: http://localhost:8000
- Documentación interactiva (Swagger UI): http://localhost:8000/docs
- Documentación alternativa (ReDoc): http://localhost:8000/redoc
- Autenticación: No requerida

---

## Uso Rápido

### Endpoint raíz (Bienvenida)

```bash
curl http://localhost:8000/
```

**Respuesta (200 OK)**:
```json
{
  "message": "Welcome to Divisas API",
  "docs": "Visita /docs para ver la documentación interactiva",
  "version": "1.0.0"
}
```

### Consultar una divisa

```bash
curl http://localhost:8000/api/divisas/USD
```

**Respuesta (200 OK)**:
```json
{
  "symbol": "$",
  "name": "US Dollar",
  "code": "USD"
}
```

---

## Endpoints

### GET /

**Descripción**: Punto de entrada (bienvenida) de la API.

**Método**: `GET`  
**Ruta**: `/`  
**Autenticación**: No requerida  
**Parámetros**: Ninguno

**Respuesta (200 OK)**:
```json
{
  "message": "Welcome to Divisas API",
  "docs": "Visita /docs para ver la documentación interactiva",
  "version": "1.0.0"
}
```

---

### GET /api/divisas/{code}

**Descripción**: Obtener información detallada de una divisa específica.

**Método**: `GET`  
**Ruta**: `/api/divisas/{code}`  
**Autenticación**: No requerida

**Parámetros**:

| Nombre | Tipo | Requerido | Descripción | Ejemplo |
|--------|------|-----------|-------------|---------|
| `code` | string | Sí | Código ISO de la divisa (3 letras) | `USD`, `EUR`, `GBP` |

**Respuesta (200 OK)**:
```json
{
  "symbol": "$",
  "name": "US Dollar",
  "code": "USD"
}
```

---

## Ejemplos de Uso

### Ejemplo 1: GET a localhost - USD

**Petición HTTP**:
```bash
curl -X GET "http://localhost:8000/api/divisas/USD" \
  -H "Accept: application/json"
```

**Detalles de la petición**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Local | `http://localhost:8000/api/divisas/USD` |
| Parámetro Path | `code=USD` |

**Respuesta (200 OK)**:
```json
{
  "symbol": "$",
  "name": "US Dollar",
  "code": "USD"
}
```

---

### Ejemplo 2: GET a localhost - EUR (Euro)

**Petición HTTP**:
```bash
curl -X GET "http://localhost:8000/api/divisas/EUR" \
  -H "Accept: application/json"
```

**Detalles de la petición**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Local | `http://localhost:8000/api/divisas/EUR` |
| Parámetro Path | `code=EUR` |

**Respuesta (200 OK)**:
```json
{
  "symbol": "€",
  "name": "Euro",
  "code": "EUR"
}
```

---

### Ejemplo 3: GET a localhost - GBP (Libra Esterlina)

**Petición HTTP**:
```bash
curl -X GET "http://localhost:8000/api/divisas/GBP" \
  -H "Accept: application/json"
```

**Detalles de la petición**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Local | `http://localhost:8000/api/divisas/GBP` |
| Parámetro Path | `code=GBP` |

**Respuesta (200 OK)**:
```json
{
  "symbol": "£",
  "name": "British Pound Sterling",
  "code": "GBP"
}
```

---

### Ejemplo 4: GET a localhost - JPY (Yen Japonés)

**Petición HTTP**:
```bash
curl -X GET "http://localhost:8000/api/divisas/JPY" \
  -H "Accept: application/json"
```

**Detalles de la petición**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Local | `http://localhost:8000/api/divisas/JPY` |
| Parámetro Path | `code=JPY` |

**Respuesta (200 OK)**:
```json
{
  "symbol": "¥",
  "name": "Japanese Yen",
  "code": "JPY"
}
```

---

### Ejemplo 5: Error - Código inválido

**Petición HTTP**:
```bash
curl -X GET "http://localhost:8000/api/divisas/XYZ" \
  -H "Accept: application/json"
```

**Respuesta (404 Not Found)**:
```json
{
  "detail": "Divisa 'XYZ' no encontrada. Verifica que el código ISO sea válido."
}
```

---

### Ejemplo 6: GET a la API externa - USD (Detrás de escenas)

Cuando haces GET a `http://localhost:8000/api/divisas/USD`, internamente la API local realiza una llamada GET a la API externa:

**Petición HTTP interna (desde tu servidor)**:
```bash
curl -X GET "https://api.freecurrencyapi.com/v1/currencies?currencies=USD&apikey=YOUR_API_KEY"
```

**Detalles de la petición a API externa**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Externa | `https://api.freecurrencyapi.com/v1/currencies` |
| Parámetro Query 1 | `currencies=USD` |
| Parámetro Query 2 | `apikey=YOUR_API_KEY` |

**Respuesta de la API externa (200 OK)**:
```json
{
  "data": {
    "USD": {
      "symbol": "$",
      "name": "United States Dollar",
      "code": "USD"
    }
  }
}
```

---

### Ejemplo 7: GET a la API externa - EUR (Detrás de escenas)

**Petición HTTP interna (desde tu servidor)**:
```bash
curl -X GET "https://api.freecurrencyapi.com/v1/currencies?currencies=EUR&apikey=YOUR_API_KEY"
```

**Detalles de la petición a API externa**:

| Parámetro | Valor |
|-----------|-------|
| Método HTTP | `GET` |
| URL Externa | `https://api.freecurrencyapi.com/v1/currencies` |
| Parámetro Query 1 | `currencies=EUR` |
| Parámetro Query 2 | `apikey=YOUR_API_KEY` |

**Respuesta de la API externa (200 OK)**:
```json
{
  "data": {
    "EUR": {
      "symbol": "€",
      "name": "Euro",
      "code": "EUR"
    }
  }
}
```

---

## Estructura del Proyecto

```
api_divisas/
│
├── main.py                          # Punto de entrada de la aplicación
├── appsettings.py                   # Configuración centralizada
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno (NO subir a Git)
├── .gitignore                       # Archivos ignorados por Git
├── README.md                        # Documentación
│
├── controllers/                     # Capa de presentación (API endpoints)
│   ├── __init__.py
│   └── DivisasController.py        # Endpoints de divisas
│
├── services/                        # Capa de lógica de negocio
│   ├── __init__.py
│   └── DivisaServices.py           # Lógica de obtención de divisas
│
├── clients/                         # Capa de clientes HTTP
│   ├── __init__.py
│   └── DivisaClient.py             # Cliente de freecurrencyapi.com
│
├── DTOs/                            # Modelos de datos (Data Transfer Objects)
│   ├── __init__.py
│   └── DivisaDtos.py               # Estructuras de respuesta
└── 
```

---

## Arquitectura

### Patrón: Layered Architecture (Arquitectura de Capas)

```
┌─────────────────────────────────────────────┐
│         CLIENTE HTTP (Browser/App)          │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN (Controllers)         │
│  - Recibe peticiones HTTP                   │
│  - Valida parámetros                        │
│  - Retorna respuestas JSON                  │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│  CAPA DE LÓGICA DE NEGOCIO (Services)       │
│  - Coordina operaciones                     │
│  - Transforma datos                         │
│  - Maneja validaciones                      │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│  CAPA DE CLIENTES (Clients)                 │
│  - Comunica con APIs externas               │
│  - Maneja peticiones HTTP                   │
│  - Procesa respuestas                       │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│  APIs EXTERNAS (freecurrencyapi.com)        │
│  - Proporciona datos de divisas              │
└─────────────────────────────────────────────┘
```

### Descripción de carpetas:

| Carpeta | Propósito |
|---------|----------|
| `controllers/` | Define los endpoints HTTP (rutas) |
| `services/` | Contiene la lógica de negocio |
| `clients/` | Se comunica con APIs externas |
| `DTOs/` | Define estructuras de datos |

---

### Ventajas de esta arquitectura:

- **Separación de responsabilidades** - Cada capa tiene una función clara  
- **Reutilizable** - Las capas se pueden usar en diferentes contextos  
- **Testeable** - Fácil de hacer tests unitarios  
- **Mantenible** - Cambios en una capa no afectan otras  
- **Escalable** - Fácil de agregar nuevas funcionalidades  

---

## Códigos de Error HTTP

| Código | Nombre | Descripción |
|--------|--------|-------------|
| **200** | OK | Petición exitosa, datos retornados |
| **404** | Not Found | Endpoint no existe o divisa no encontrada |
| **422** | Validation Error | Error de validación en los parámetros enviados |
| **401** | Unauthorized | Credenciales de autenticación inválidas |
| **403** | Forbidden | No tienes permiso para usar este endpoint |
| **429** | Too Many Requests | Has alcanzado tu límite de tasas o límite mensual |
| **500** | Internal Server Error | Error interno del servidor |

### Notas sobre errores:
- Si obtienes `500`, revisa que `COD_ISO_API_KEY` esté en `.env` y sea válida.
- Si obtienes `404` o `422`, verifica que el código `code` sea un código ISO válido.

---

## Códigos ISO de Divisas

| Código | Nombre | Símbolo |
|--------|--------|---------|
| AUD | Australian Dollar | $ |
| BGN | Bulgarian Lev | лв. |
| BRL | Brazilian Real | R$ |
| CAD | Canadian Dollar | $ |
| CHF | Swiss Franc | CHF |
| CNY | Chinese Yuan | ¥ |
| CZK | Czech Republic Koruna | Kč |
| DKK | Danish Krone | kr |
| EUR | Euro | € |
| GBP | British Pound Sterling | £ |
| HKD | Hong Kong Dollar | $ |
| HRK | Croatian Kuna | kn |
| HUF | Hungarian Forint | Ft |
| IDR | Indonesian Rupiah | Rp |
| ILS | Israeli New Sheqel | ₪ |
| INR | Indian Rupee | টকা |
| ISK | Icelandic Króna | kr |
| JPY | Japanese Yen | ¥ |
| KRW | South Korean Won | ₩ |
| MXN | Mexican Peso | $ |
| MYR | Malaysian Ringgit | RM |
| NOK | Norwegian Krone | kr |
| NZD | New Zealand Dollar | $ |
| PHP | Philippine Peso | ₱ |
| PLN | Polish Zloty | zł |
| RON | Romanian Leu | RON |
| RUB | Russian Ruble | руб. |
| SEK | Swedish Krona | kr |
| SGD | Singapore Dollar | $ |
| THB | Thai Baht | ฿ |
| TRY | Turkish Lira | ₺ |
| USD | US Dollar | $ |
| ZAR | South African Rand | R |

---

## Tecnologías Utilizadas

### Backend
- **FastAPI** (v0.104+) - Framework web moderno y rápido
- **Uvicorn** (v0.24+) - Servidor ASGI
- **Httpx** (v0.25+) - Cliente HTTP asíncrono
- **Pydantic** (v2.0+) - Validación de datos
- **Python** (v3.8+) - Lenguaje de programación

### Herramientas
- **python-dotenv** - Manejo de variables de entorno
- **Swagger UI** - Documentación interactiva
- **ReDoc** - Documentación alternativa

### APIs Externas
- **freecurrencyapi.com** - Datos de divisas

## Soporte

Si tienes preguntas o necesitas ayuda:

1. Revisa la documentación en `/docs` (Swagger UI)
2. Consulta los comentarios en el código fuente
3. Revisa la sección de **Códigos de Error HTTP**
4. Contacta al autor

---

## Autor

**Nombre**: Jesnayder Pedrozo Huertas  
**Organización**: Corporación Universitaria Americana  
**Programa**: Diplomado .NET  
**Fecha**: Enero 2026  
**Email**: jesnayder_pedrozo6962@americana.edu.co

---
