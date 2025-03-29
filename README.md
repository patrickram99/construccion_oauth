# Servidor OAuth con CRUD PostgreSQL

## Ejemplos 

### 1. Obtener Token
- **Solicitud**: 
  - POST a `http://localhost:5000/token`
  - Cuerpo (JSON): 
    ```
    {
        "client_id": "test_client", 
        "client_secret": "test_secret"
    }
    ```
- **Respuesta**:
  ```
  {
      "token_acceso": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "tipo_token": "bearer",
      "expira_en": 3600
  }
  ```

### 2. Crear Producto
- **Solicitud**:
  - POST a `http://localhost:5001/api/productos`
  - Encabezados: `Authorization: Bearer tu_token_aquí`
  - Cuerpo (JSON):
    ```
    {
        "nombre": "Producto de Prueba",
        "descripcion": "Este es un producto de prueba"
    }
    ```
- **Respuesta**:
  ```
  {
      "id": 1,
      "nombre": "Producto de Prueba",
      "descripcion": "Este es un producto de prueba",
      "fecha_creacion": "2025-03-29T10:15:30.123456"
  }
  ```

### 3. Obtener Todos los Productos
- **Solicitud**:
  - GET a `http://localhost:5001/api/productos`
  - Encabezados: `Authorization: Bearer tu_token_aquí`
- **Respuesta**:
  ```
  [
      {
          "id": 1,
          "nombre": "Producto de Prueba",
          "descripcion": "Este es un producto de prueba",
          "fecha_creacion": "2025-03-29T10:15:30.123456"
      }
  ]
  ```

### 4. Obtener un Producto Específico
- **Solicitud**:
  - GET a `http://localhost:5001/api/productos/1`
  - Encabezados: `Authorization: Bearer tu_token_aquí`
- **Respuesta**:
  ```
  {
      "id": 1,
      "nombre": "Producto de Prueba",
      "descripcion": "Este es un producto de prueba",
      "fecha_creacion": "2025-03-29T10:15:30.123456"
  }
  ```

### 5. Actualizar Producto
- **Solicitud**:
  - PUT a `http://localhost:5001/api/productos/1`
  - Encabezados: `Authorization: Bearer tu_token_aquí`
  - Cuerpo (JSON):
    ```
    {
        "nombre": "Producto Actualizado",
        "descripcion": "Este producto ha sido actualizado"
    }
    ```
- **Respuesta**:
  ```
  {
      "id": 1,
      "nombre": "Producto Actualizado",
      "descripcion": "Este producto ha sido actualizado",
      "fecha_creacion": "2025-03-29T10:15:30.123456"
  }
  ```

### 6. Eliminar Producto
- **Solicitud**:
  - DELETE a `http://localhost:5001/api/productos/1`
  - Encabezados: `Authorization: Bearer tu_token_aquí`
- **Respuesta**:
  ```
  {
      "mensaje": "Producto 1 eliminado con éxito"
  }
  ```
