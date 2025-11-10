# User Service

Microservicio para gestión de usuarios en la arquitectura de tienda de libros.

## Características

- **Autenticación JWT**: Sistema de autenticación basado en tokens
- **Gestión de usuarios**: CRUD completo de usuarios
- **Control de acceso**: Roles y permisos
- **Perfiles de usuario**: Información detallada de clientes
- **Spring Boot**: Framework Java empresarial
- **PostgreSQL**: Base de datos relacional

## Tecnologías

- Java 17
- Spring Boot 3.2.0
- Spring Security
- Spring Data JPA
- JWT (JSON Web Tokens)
- PostgreSQL
- Maven

## Endpoints

### Authentication
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/validate` - Validar token JWT

### Users
- `GET /api/users/me` - Obtener usuario actual
- `GET /api/users/{id}` - Obtener usuario por ID
- `GET /api/users` - Listar todos los usuarios (Admin)
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario (Admin)
- `POST /api/users/{id}/activate` - Activar usuario (Admin)
- `POST /api/users/{id}/deactivate` - Desactivar usuario (Admin)

### Health
- `GET /api/health` - Health check
- `GET /api/health/live` - Liveness probe
- `GET /api/health/ready` - Readiness probe

## Variables de Entorno

```bash
DB_URL=jdbc:postgresql://localhost:5432/userdb
DB_USERNAME=postgres
DB_PASSWORD=postgres
JWT_SECRET=your-secret-key
```

## Ejecución Local

```bash
# Compilar
mvn clean install

# Ejecutar
mvn spring-boot:run

# Con perfil de desarrollo (H2)
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

## Docker

```bash
# Construir imagen
docker build -t user-service:latest .

# Ejecutar contenedor
docker run -p 8080:8080 \
  -e DB_URL=jdbc:postgresql://postgres:5432/userdb \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  user-service:latest
```

## Comunicación

Este servicio utiliza **comunicación REST directa** (no RabbitMQ) para operaciones síncronas de autenticación y gestión de usuarios.



