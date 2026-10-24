# INFORME FINAL - Sistema de Reservas Académicas

## 1. Objetivo y alcance del proyecto

**Objetivo:** Centralizar las reservas de laboratorios, auditorios y salas de cómputo, evitando solicitudes duplicadas, conflictos de horarios y dificultades para consultar disponibilidad, mediante una aplicación web académica.

**Alcance:**
- Gestión de espacios académicos (laboratorios, auditorios, salas de cómputo)
- Registro y administración de usuarios con roles (Administrador / Solicitante)
- Creación de solicitudes de reserva
- Consulta y validación de disponibilidad
- Prevención de reservas superpuestas y simultáneas
- Aprobación y rechazo de solicitudes
- Cancelación (con reglas diferenciadas) e historial de reservas

**Fuera de alcance inicial:**
- Límite de máximo cuatro horas consecutivas (se incorporará como cambio independiente gestionado con OpenSpec)
- Integraciones externas (LDAP, correo, calendarios)
- Aplicación móvil nativa
- Despliegue automatizado complejo

## 2. Arquitectura y tecnologías utilizadas

**Arquitectura:** Aplicación web modular con patrón App Factory y Blueprints (Flask). Separación por capas: modelos, servicios, rutas (blueprints), plantillas, utilidades.

**Tecnologías:**
- Backend: Python, Flask 3.0.3
- ORM/Persistencia: Flask-SQLAlchemy 3.1.1, SQLite
- Autenticación: Flask-Login 3.1.1
- Seguridad: Werkzeug 3.0.3 (hash de contraseñas)
- Frontend: HTML, CSS (plantillas Jinja2)
- Pruebas: pytest 8.3.2, pytest-flask 1.3.0

**Estructura implementada:**
- `app/__init__.py` (app factory)
- `app/auth/`, `app/spaces/`, `app/reservations/`, `app/admin/` (blueprints)
- `app/models/` (User, Space, Reservation)
- `app/services/` (AuthService, UserService)
- `app/utils/decorators.py` (control de acceso por roles)
- `app/templates/` y `app/static/` (interfaz web)
- `tests/` (unitarias)

## 3. Funcionalidades implementadas y pendientes

### Implementadas (en desarrollo funcional parcial / base)
- **Estructura base:** App factory, blueprints, configuración, base de datos SQLite en memoria/archivo
- **Usuarios y roles:** Modelo User con roles `administrador`/`solicitante`, hash de contraseñas, autenticación, decoradores de acceso por rol
- **Servicios:** `AuthService` (registro/autenticación), `UserService` (listado/filtros, cambio de rol, activación/desactivación)
- **Espacios:** Modelo `Space` (tipo, capacidad, ubicación, estado)
- **Reservas:** Modelo `Reservation` con estados, trazabilidad (decisor/autorizante/cancelación), campo para marcar conflictos
- **Interfaz web:** Plantillas base con navegación, páginas para inicio/espacios/reservas/administración/login con estilos CSS
- **Pruebas unitarias básicas:** Creación de app, autenticación, gestión de usuarios/roles, decoradores

### Pendientes (según `tasks.md`)
- **Espacios (CRUD completo):** Crear/editar/activar/desactivar espacios para administrador con validación; impedir desactivación si hay reservas aprobadas futuras
- **Reservas (lógica completa):** Creación con marcado de conflictos para pendientes solapados; transacciones con `BEGIN IMMEDIATE`, revalidación, reintentos limitados; aprobación bloqueada si hay conflicto con aprobadas
- **Cancelación:** Solicitante solo pendientes; aprobadas solo con autorización administrativa con registro
- **Historial:** Consulta con filtros y trazabilidad completa
- **Pruebas de integración:** Flujos completos, concurrencia, control de acceso por roles

## 4. Cómo se aplicó SDD con OpenSpec

- **Inicialización:** Se usó OpenSpec en el proyecto (presente en `openspec/`). Configuración en `openspec/config.yaml` con schema `spec-driven`.
- **Cambio creado:** Se generó el cambio `sistema-reservas-academicas` con todos los artefactos en una sola propuesta.
- **Artefactos generados:** `proposal.md`, `specs/spaces/spec.md`, `specs/users-roles/spec.md`, `specs/reservations/spec.md`, `design.md`, `tasks.md`.
- **Flujo:** Proposal → Specs (delta por capacidad) → Design (decisiones técnicas) → Tasks (descomposición verificable). 
- **Aplicación:** Se inició `/opsx:apply` de forma progresiva siguiendo el orden de `tasks.md`.

## 5. Cómo se revisaron las especificaciones antes de programar

- **Revisión con decisiones:** Se aplicaron decisiones explícitas antes de implementar:
  1. Cancelación: pendientes por solicitante; aprobadas solo con autorización administrativa
  2. Pendientes solapados: permitir crear pero marcar como conflicto para revisión; no aprobar si hay conflicto con aprobadas
  3. Desactivación de espacios: impedir si hay reservas aprobadas futuras
  4. Concurrencia SQLite: `BEGIN IMMEDIATE`, revalidación dentro de transacción, reintentos limitados, errores controlados (sin afirmar garantía hasta pruebas)
  5. Límite de 4 horas: NO incluir en implementación inicial, se gestionará como cambio independiente
- **Actualización de artefactos:** Se modificaron proposal, specs, design y tasks para reflejar las decisiones.
- **Validación:** Se confirmó que no hay contradicciones pendientes y que las tareas cubren requisitos y pruebas antes de aplicar.

## 6. Gestión del cambio del límite de cuatro horas

- **Decisión:** NO se implementó. 
- **Justificación:** Requisito explícito del usuario y de las instrucciones (se incorporará después como cambio formal gestionado mediante OpenSpec).
- **Estado:** Pendiente para un cambio independiente de OpenSpec.

## 7. Pruebas ejecutadas, resultados reales y limitaciones

**Pruebas ejecutadas (reales):**
```bash
py -m pytest tests/unit/test_app_init.py -v
# Resultado: 1 passed

py -m pytest tests/unit/test_auth.py -v
# Resultado: 3 passed

py -m pytest tests/unit/test_users_roles.py -v
# Resultado: 3 passed

py -m pytest tests/unit/test_decorators.py -v
# Resultado: 1 passed
```

**Total:** 8 pruebas unitarias pasaron. Existen warnings por uso de `datetime.utcnow()` (legacy) y `Query.get()` (SQLAlchemy 2.0).

**Limitaciones:**
- Solo pruebas unitarias básicas ejecutadas. Faltan pruebas de integración y pruebas específicas de concurrencia/solapamientos/cancelación/autorización.
- La garantía de concurrencia con SQLite NO ha sido verificada aún (solo se implementará con la lógica de transacciones).
- Muchas funcionalidades están en modelo/servicio parcial o solo estructura; las rutas/plantillas muestran estado en desarrollo.

## 8. Diferencias entre la planificación inicial y la implementación final

| Aspecto | Planificación inicial | Implementación final |
|---|---|---|
| Solapamientos | Impedir crear solicitudes que se solapen con aprobadas o en conflicto | Permitir pendientes solapados marcándolos como conflicto para revisión; bloquear aprobación si hay conflicto con aprobadas |
| Cancelación | Cancelación en estados permitidos | Solicitante solo pendientes; aprobadas solo con autorización administrativa con trazabilidad |
| Desactivación espacios | Advertir/requerir confirmación | Impedir si hay reservas aprobadas futuras |
| Concurrencia | Proteger contra reservas simultáneas | Especificado con `BEGIN IMMEDIATE`, revalidación, reintentos limitados, errores controlados (pendiente de pruebas) |
| Límite 4 horas | Mencionado para futuro | Excluido explícitamente de esta implementación |

## 9. Dificultades encontradas y decisiones técnicas modificadas

**Dificultades:**
- Relaciones múltiples en SQLAlchemy entre `User` y `Reservation` (decisor, cancelador, solicitante) requirió especificar `foreign_keys`.
- Entorno Windows (PowerShell) con comandos shell distintos a bash.
- Dependencias (`pytest`, etc.) no instaladas inicialmente.
- Diseño de rutas/plantillas para mostrar interfaz funcional sin lógica completa aún.

**Decisiones modificadas:**
- Política de solapamientos más estricta en aprobación pero permisiva en creación de pendientes (marcado como conflicto).
- Cancelación diferenciada con autorización administrativa para aprobadas.
- Estrategia de concurrencia explícita con reintentos limitados y sin garantía afirmada hasta pruebas.

## 10. Ventajas y limitaciones de SDD frente a programar mediante instrucciones directas a una IA

### Ventajas
- **Claridad:** Especificaciones obligan a definir comportamiento observable, escenarios y reglas antes de codificar.
- **Trazabilidad:** Proposal/Specs/Design/Tasks conectan requisitos con verificación.
- **Revisabilidad:** Permite corregir decisiones antes de implementación (caso de las reglas de cancelación/solapamientos).
- **Consistencia:** Reduce ambigüedad y contradicciones entre funcionalidades.
- **Verificabilidad:** Las tareas incluyen criterios de verificación y facilitan pruebas.

### Limitaciones
- **Sobrecarga inicial:** Requiere tiempo para generar y revisar artefactos.
- **Rigidez:** Cambiar reglas después requiere actualizar specs/design/tasks.
- **Curva de aprendizaje:** Requiere entender el flujo OpenSpec.
- **No elimina errores:** Especificaciones mal revisadas se traducen a código mal implementado.
- **Dependiente de revisión humana:** Las decisiones críticas requieren intervención humana.

## 11. Conclusiones personales

- **Importancia de la revisión:** Las decisiones aplicadas antes de codificar evitaron implementar reglas incorrectas.
- **SDD efectivo:** OpenSpec ayudó a estructurar el problema y mantener coherencia entre requisitos, diseño y tareas.
- **Implementación incremental:** Enfoque progresivo con pruebas parciales es adecuado, pero falta completar lógica y pruebas de integración.
- **SQLite y concurrencia:** Requiere cuidado con transacciones; la advertencia de "no afirmar garantía hasta pruebas" es correcta.
- **Documentación:** Es fundamental distinguir lo terminado de lo pendiente y no inventar resultados.
- **Trabajo futuro:** Completar CRUD de espacios, lógica completa de reservas con transacciones, pruebas de integración/concurrencia y, posteriormente, gestionar el límite de 4 horas como cambio independiente con OpenSpec.

---

**Nota:** Este informe refleja el estado real al momento de redacción. No se inventan pruebas, commits, capturas ni funcionalidades completadas. Las funcionalidades marcadas como "pendientes" corresponden a las tareas no completadas en `tasks.md`.
