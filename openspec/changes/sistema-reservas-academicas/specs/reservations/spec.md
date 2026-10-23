# Spec Delta

## Purpose

Gestionar el ciclo completo de solicitudes de reserva: creación, validación de disponibilidad, prevención de solapamientos, aprobación/rechazo, cancelación e historial de reservas.

## ADDED Requirements

### Requirement: Crear solicitud de reserva
El sistema SHALL permitir a usuarios con rol Solicitante crear solicitudes de reserva especificando espacio, fecha, hora de inicio y hora de fin.

#### Scenario: Creación exitosa de solicitud
- **WHEN** un Solicitante proporciona datos válidos para una solicitud
- **THEN** el sistema crea la solicitud en estado Pendiente
- **AND** registra fecha/hora de creación y usuario solicitante
- **AND** valida disponibilidad antes de crearla

#### Scenario: Creación con datos inválidos
- **WHEN** un Solicitante proporciona horarios inválidos (fin <= inicio)
- **THEN** el sistema rechaza la solicitud
- **AND** muestra mensaje de error claro

### Requirement: Validación de disponibilidad y prevención de solapamientos
El sistema SHALL validar la disponibilidad del espacio en el intervalo solicitado e impedir reservas superpuestas con reservas aprobadas o en conflicto.

#### Scenario: Solicitud con solapamiento a reserva aprobada
- **WHEN** un Solicitante solicita un intervalo que se solapa con una reserva ya Aprobada
- **THEN** el sistema rechaza la solicitud
- **AND** indica que existe conflicto de horario
- **AND** no crea la solicitud

#### Scenario: Solicitud con solapamiento a otra solicitud pendiente
- **WHEN** un Solicitante solicita un intervalo que se solapa con otra solicitud en estado Pendiente
- **THEN** el sistema rechaza la solicitud o marca conflicto según política
- **AND** previene doble asignación del mismo espacio en el mismo intervalo
- **AND** protege contra reservas simultáneas mediante control transaccional

#### Scenario: Espacio inactivo
- **WHEN** un Solicitante intenta reservar un espacio con estado Inactivo
- **THEN** el sistema rechaza la solicitud
- **AND** informa que el espacio no está disponible

### Requirement: Aprobación y rechazo de solicitudes
El sistema SHALL permitir al Administrador aprobar o rechazar solicitudes pendientes, registrando quién, cuándo y motivo.

#### Scenario: Aprobar solicitud válida
- **WHEN** un Administrador aprueba una solicitud Pendiente válida
- **THEN** el sistema cambia el estado a Aprobada
- **AND** registra administrador, fecha/hora de decisión
- **AND** bloquea ese intervalo para nuevas solicitudes conflictivas

#### Scenario: Rechazar solicitud con motivo
- **WHEN** un Administrador rechaza una solicitud Pendiente
- **THEN** el sistema solicita o registra motivo de rechazo
- **AND** cambia el estado a Rechazada
- **AND** registra administrador, fecha/hora y motivo
- **AND** notifica al solicitante (en la interfaz)

#### Scenario: No aprobar solicitud ya procesada
- **WHEN** un Administrador intenta aprobar/rechazar una solicitud ya procesada
- **THEN** el sistema rechaza la acción
- **AND** informa que la solicitud ya fue procesada

### Requirement: Cancelación e historial de reservas
El sistema SHALL permitir la cancelación de solicitudes en estados permitidos y proporcionar historial con filtros.

#### Scenario: Cancelar solicitud propia pendiente
- **WHEN** un Solicitante cancela su propia solicitud en estado Pendiente
- **THEN** el sistema cambia el estado a Cancelada
- **AND** registra fecha/hora de cancelación
- **AND** libera el intervalo si aplica

#### Scenario: No cancelar solicitud ajena
- **WHEN** un Solicitante intenta cancelar una solicitud de otro usuario
- **THEN** el sistema deniega la acción
- **AND** no modifica el estado

#### Scenario: No cancelar reserva ya aprobada sin política especial
- **WHEN** un Solicitante intenta cancelar una solicitud ya Aprobada
- **THEN** el sistema deniega la cancelación o requiere autorización según política
- **AND** informa las restricciones al usuario

#### Scenario: Consultar historial con filtros
- **WHEN** un usuario consulta su historial de reservas
- **THEN** el sistema muestra solicitudes con estados, fechas, espacio y detalles
- **AND** permite filtrar por estado, fecha o espacio

#### Scenario: Historial completo para administrador
- **WHEN** un Administrador consulta el historial general
- **THEN** el sistema muestra todas las solicitudes con solicitante, administrador decisor y trazabilidad completa
