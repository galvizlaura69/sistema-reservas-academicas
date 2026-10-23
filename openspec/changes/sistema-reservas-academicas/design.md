# Design

## Context

Ver proposal.md para la motivación. Este diseño se basa en los requisitos especificados en `specs/spaces/`, `specs/users-roles/` y `specs/reservations/`. Se requiere una aplicación web académica con Python, Flask, SQLite, HTML/CSS y pruebas con pytest, siguiendo la arquitectura propuesta en PLAN_INGENIERIA.md.

## Goals / Non-Goals

**Goals:**
- Implementar arquitectura modular en Flask (aplicación factory, blueprints, modelos, servicios, validadores)
- Diseñar esquema de datos en SQLite con integridad referencial
- Garantizar prevención de solapamientos y protección contra reservas simultáneas
- Aplicar control de acceso basado en roles
- Mantener trazabilidad (quién, cuándo, motivos)
- Facilitar pruebas unitarias/integración con pytest

**Non-Goals:**
- Implementar la restricción "máximo cuatro horas consecutivas" (se gestionará como cambio formal con OpenSpec más adelante)
- Integraciones con sistemas externos (LDAP, correo, calendarios)
- Aplicación móvil nativa
- Despliegue a producción automatizado complejo (se considera básico)

## Decisions

### Decisión 1: Arquitectura - Aplicación Factory + Blueprints
- **Razón**: Permite modularidad, testabilidad y configuración por entorno.
- **Alternativas consideradas**:
  - Monolito plano (app.py único): más simple pero menos escalable y difícil de testear.
  - Blueprints sin factory: limita configuración y pruebas.
- **Elegida**: `create_app()` con blueprints por módulo (auth, spaces, reservations, admin).

### Decisión 2: Persistencia - SQLite con SQLAlchemy/SQLite nativo
- **Razón**: Requisito explícito (SQLite), ligero, adecuado para entorno académico.
- **Alternativas consideradas**:
  - PostgreSQL: más robusto pero requiere servidor, no especificado.
  - JSON files: sin integridad referencial, difícil para concurrencia.
- **Elegida**: SQLite con SQLAlchemy para ORM y migraciones básicas, o SQL directo con transacciones. Priorizar transacciones para prevenir reservas simultáneas.

### Decisión 3: Prevención de solapamientos y concurrencia
- **Razón**: Crítico para integridad del sistema.
- **Alternativas consideradas**:
  - Validación solo en aplicación sin locks: vulnerable a race conditions.
  - Locks a nivel de tabla/registro con transacciones: necesario.
- **Elegida**: Validación con consulta de solapamientos + transacciones con `BEGIN IMMEDIATE` o equivalente en SQLite. Usar constraints cuando sea posible y validación en servicio con bloqueo.

### Decisión 4: Control de acceso
- **Razón**: Requisito de roles y permisos.
- **Alternativas consideradas**:
  - Decoradores simples por rol: suficiente para esta fase.
  - Sistema de permisos granulares: excesivo para dos roles.
- **Elegida**: Decoradores `@login_required`, `@role_required('admin')`/`@role_required('solicitante')`.

### Decisión 5: Modelado de datos
- **Entidades principales**:
  - `User` (id, nombre, email, password_hash, role, active, created_at)
  - `Space` (id, name, type, capacity, location, status, description, created_at, updated_at)
  - `Reservation` (id, space_id, user_id, start_time, end_time, status, reason, admin_id, decision_at, cancelled_at, created_at)
- **Razón**: Cubre todos los requisitos con trazabilidad completa.
- **Alternativas consideradas**:
  - Estados como enum en texto: SQLite no tiene enum nativo, usar CHECK o strings validados.
- **Elegida**: Campos con validación en aplicación y CHECK constraints donde aplique.

## Risks / Trade-offs

- **Riesgo**: Condiciones de carrera en reservas simultáneas → **Mitigación**: Usar transacciones con bloqueo, validar dentro de transacción, tests de concurrencia.
- **Riesgo**: SQLite con alta concurrencia limitada → **Mitigación**: Adecuado para uso académico; usar WAL mode y transacciones cortas.
- **Riesgo**: Validación de solapamientos compleja con zonas horarias → **Mitigación**: Usar timestamps naive UTC o naive local consistente, documentar en diseño.
- **Riesgo**: Desactivar espacio con reservas aprobadas → **Mitigación**: Validación previa, advertencia, no eliminación automática.
- **Riesgo**: Escalabilidad futura → **Mitigación**: Arquitectura modular permite migración a PostgreSQL si necesario.
- **Trade-off**: ORM vs SQL directo → **Decisión**: SQLAlchemy ofrece balance entre productividad y control transaccional.
