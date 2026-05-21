# Proyecto Microservicios

Proyecto desarrollado con arquitectura de microservicios usando Python, Flask, Docker y MySQL.  
Cuenta con dos servicios independientes que se comunican entre sí mediante APIs REST.

---

# Objetivo

Simular una arquitectura SOA/Microservicios donde:

- **Usuario Service** administra usuarios
- **Pedido Service** administra pedidos
- **Pedido Service** valida la existencia del usuario antes de crear un pedido
- Persistencia de datos usando **MySQL dockerizado**
- Documentación de endpoints con **Swagger/OpenAPI**

---

# Tecnologías utilizadas

- Python 3
- Flask
- Flask-RESTX
- SQLAlchemy
- PyMySQL
- Requests
- Docker
- Docker Compose
- MySQL 5.7
- Swagger/OpenAPI
- APIs REST
- JSON

---

# Arquitectura del proyecto

El sistema está compuesto por 3 contenedores Docker:

1. **mysql_microservicios**
   - Base de datos MySQL
   - Persistencia real de datos

2. **usuario_service**
   - Gestión de usuarios
   - Conectado a MySQL
   - API REST independiente

3. **pedido_service**
   - Gestión de pedidos
   - Conectado a MySQL
   - Se comunica con Usuario Service para validar usuarios

---

# Microservicios

## Usuario Service

Permite:

- Crear usuarios
- Obtener todos los usuarios
- Buscar usuario por ID

Puerto:

```bash
5000
```

Swagger:

```bash
http://localhost:5000/swagger
```

---

## Pedido Service

Permite:

- Crear pedidos
- Obtener todos los pedidos
- Buscar pedido por ID
- Validar usuario antes de registrar pedido

Puerto:

```bash
5001
```

Swagger:

```bash
http://localhost:5001/swagger
```

---

# Requisitos previos

Antes de ejecutar el proyecto tener instalado:

- Docker Desktop
- Docker Compose
- Python 3 (opcional, si se desea correr localmente)

Verificar Docker:

```bash
docker --version
docker compose version
```

---

# Instalación y ejecución

## 1. Abrir terminal

Ubicarse en la carpeta raíz del proyecto:

```bash
cd microservicios
```

---

## 2. Levantar contenedores

Ejecutar:

```bash
docker compose up --build
```

Esto levantará:

- MySQL
- Usuario Service
- Pedido Service

---

## 3. Verificar que todo esté corriendo

Comprobar contenedores:

```bash
docker ps
```

Deben aparecer:

- mysql_microservicios
- usuario_service
- pedido_service

---

# Uso del sistema

## Swagger Usuario Service

Abrir:

```bash
http://localhost:5000/swagger
```

---

## Swagger Pedido Service

Abrir:

```bash
http://localhost:5001/swagger
```

---

# Endpoints

# Usuario Service

## Crear usuario

POST `/usuarios`

Body:

```json
{
  "id": 1,
  "nombre": "Juan",
  "email": "juan@gmail.com",
  "password": "123456"
}
```

---

## Obtener todos los usuarios

GET `/usuarios`

---

## Buscar usuario por ID

GET `/usuarios/1`

---

# Pedido Service

## Crear pedido

POST `/pedidos`

Body:

```json
{
  "id": 1,
  "usuario_id": 1,
  "producto": "Notebook",
  "cantidad": 2,
  "estado": "pendiente"
}
```

---

## Obtener todos los pedidos

GET `/pedidos`

---

## Buscar pedido por ID

GET `/pedidos/1`

---

# Validación entre microservicios

Antes de crear un pedido, **Pedido Service** consulta a **Usuario Service**.

Si el usuario no existe:

```json
{
  "error": "El usuario no existe"
}
```

Esto demuestra comunicación **Backend ↔ Backend**.

---

# Persistencia de datos

Los datos se almacenan en MySQL dentro de Docker.

Puede probarse:

1. Crear usuario
2. Crear pedido
3. Ejecutar:

```bash
docker compose down
```

4. Levantar nuevamente:

```bash
docker compose up
```

5. Consultar nuevamente el usuario o pedido

Si siguen existiendo, la persistencia funciona correctamente.

---

# Logs útiles

Ver logs de todos los servicios:

```bash
docker compose logs
```

Ver logs de Pedido Service:

```bash
docker compose logs pedido-service --tail=50
```

Ver logs de Usuario Service:

```bash
docker compose logs usuario-service --tail=50
```

---

# Detener proyecto

Para apagar los contenedores:

```bash
docker compose down
```

---

# Funcionalidades implementadas

- Arquitectura de microservicios
- APIs REST
- Swagger/OpenAPI
- JSON
- Comunicación entre servicios
- Validación entre microservicios
- Persistencia real con MySQL
- Docker Compose
- Servicios independientes
- Escalabilidad básica
- SOA (Service Oriented Architecture)

---

# Estado del proyecto

Proyecto funcional y listo para pruebas o entrega académica.