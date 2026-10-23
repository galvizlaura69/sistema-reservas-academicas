# Tasks

## 1. Configuración y estructura del proyecto

- [ ] 1.1 Crear estructura modular de Flask (app factory, blueprints, config, __init__.py) y verificar que la app se inicializa correctamente con pytest
- [ ] 1.2 Configurar base de datos SQLite con SQLAlchemy, crear esquema inicial y verificar conexión exitosa
- [ ] 1.3 Configurar pruebas con pytest (conftest, fixtures de app/db) y verificar que las pruebas base corren

## 2. Gestión de usuarios, roles y autenticación

- [ ] 2.1 Implementar modelo User con roles (Administrador/Solicitante), hash de contraseñas y validación, verificando con pruebas unitarias
- [ ] 2.2 Implementar registro, login, logout con control de acceso por roles (decoradores) y verificar flujos con pruebas
- [ ] 2.3 Implementar administración de usuarios (listar, activar/desactivar, cambiar rol) para Administrador y verificar permisos con pruebas

## 3. Gestión de espacios académicos

- [ ] 3.1 Implementar modelo Space (tipo, capacidad, ubicación, estado) con validaciones y verificar con pruebas unitarias
- [ ] 3.2 Implementar CRUD de espacios para Administrador (crear, editar, activar/desactivar) y verificar con pruebas
- [ ] 3.3 Implementar consulta de espacios y filtrado por disponibilidad para usuarios autenticados y verificar con pruebas

## 4. Solicitudes de reserva - Creación y validación

- [ ] 4.1 Implementar modelo Reservation con estados (Pendiente/Aprobada/Rechazada/Cancelada), campo de conflicto/marcado, timestamps y trazabilidad, verificando con pruebas unitarias
- [ ] 4.2 Implementar servicio de validación de disponibilidad con transacciones `BEGIN IMMEDIATE`, revalidación dentro de la transacción, marcado de conflictos para pendientes solapados, y manejo de errores de bloqueo con reintentos limitados; verificar con pruebas de concurrencia (sin afirmar garantía hasta pasar pruebas)
- [ ] 4.3 Implementar creación de solicitudes de reserva por Solicitante con validaciones (permitir solapamiento con pendientes marcando conflicto) y verificar comportamiento según reglas

## 5. Aprobación, rechazo, cancelación e historial

- [ ] 5.1 Implementar aprobación/rechazo de solicitudes por Administrador con registro de decisor, fecha/hora y motivo; bloquear aprobación si hay conflicto con reservas aprobadas, verificando con pruebas
- [ ] 5.2 Implementar cancelación: Solicitante puede cancelar solo pendientes; reservas aprobadas solo con autorización administrativa, con registro de autorizante/motivo/fecha; verificar restricciones con pruebas
- [ ] 5.3 Implementar historial de reservas (propio y general) con filtros y trazabilidad completa (solicitante, decisor/autorizante, motivos), verificando con pruebas de integración

## 6. Pruebas de integración y validación final

- [ ] 6.1 Implementar pruebas de integración cubriendo flujos completos (crear solicitud → aprobar → historial, incluyendo cancelación) y verificar que todas pasan
- [ ] 6.2 Verificar prevención de solapamientos: permitir pendientes solapados con marcado de conflicto, bloquear aprobación con reservas aprobadas, y protección contra concurrencia con `BEGIN IMMEDIATE` y reintentos
- [ ] 6.3 Verificar desactivación de espacios (imposible si hay reservas aprobadas futuras) y cancelación según política
- [ ] 6.4 Verificar control de acceso basado en roles en todos los endpoints críticos
- [ ] 6.5 Ejecutar suite completa de pruebas (pytest) y verificar cobertura de casos principales definidos en las especificaciones; NO afirmar garantía de concurrencia hasta que las pruebas específicas lo validen
