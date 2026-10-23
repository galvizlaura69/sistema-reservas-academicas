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
El sistema SHALL validar la disponibilidad del espacio en el intervalo solicitado. Las solicitudes pendientes que se solapen entre sí podrán registrarse pero se marcarán como conflicto para revisión administrativa. No se permitirá aprobar una solicitud si existe otra reserva ya aprobada para el mismo espacio y horario. Las operaciones de reserva se realizarán dentro de transacciones con `BEGIN IMMEDIATE`, revalidando la disponibilidad dentro de la transacción antes de confirmar. Los errores de bloqueo se manejarán con reintentos limitados y errores controlados. La garantía de concurrencia NO se afirmará hasta ser verificada mediante pruebas.

#### Scenario: Solicitud con solapamiento a reserva aprobada (al crear)
- **WHEN** un Solicitante solicita un intervalo que se solapa con una reserva ya Aprobada
- **THEN** el sistema registra la solicitud en estado Pendiente
- **AND** la marca con indicador de conflicto por solapamiento con reserva aprobada
- **AND** no bloquea automáticamente la creación, pero quedará en revisión administrativa

#### Scenario: Solicitud con solapamiento a otra solicitud pendiente
- **WHEN** un Solicitante solicita un intervalo que se solapa con otra solicitud en estado Pendiente
- **THEN** el sistema registra la solicitud en estado Pendiente
- **AND** marca ambas solicitudes como en conflicto para revisión administrativa
- **AND** protege contra reservas simultáneas mediante transacciones con BEGIN IMMEDIATE y revalidación dentro de la transacción

#### Scenario: Intento de aprobación con conflicto a reserva aprobada
- **WHEN** un Administrador intenta aprobar una solicitud que se solapa con otra reserva ya Aprobada para el mismo espacio y horario
- **THEN** el sistema rechaza la aprobación
- **AND** informa que existe un conflicto con una reserva aprobada
- **AND** la solicitud permanece en estado Pendiente o se mantiene en revisión

#### Scenario: Espacio inactivo
- **WHEN** un Solicitante intenta reservar un espacio con estado Inactivo
- **THEN** el sistema rechaza la solicitud
- **AND** informa que el espacio no está disponible

#### Scenario: Error de bloqueo por concurrencia
- **WHEN** ocurre un error de bloqueo al intentar crear o aprobar una reserva en una transacción
- **THEN** el sistema reintenta la operación un número limitado de veces
- **AND** si no logra adquirir el bloqueo, devuelve un error controlado al usuario
- **AND** no confirma la reserva

### Requirement: Aprobación y rechazo de solicitudes
El sistema SHALL permitir al Administrador aprobar o rechazar solicitudes pendientes, registrando quién, cuándo y motivo. La aprobación solo será posible si no existe conflicto con reservas ya aprobadas.

#### Scenario: Aprobar solicitud válida sin conflictos
- **WHEN** un Administrador aprueba una solicitud Pendiente sin solapamiento con reservas Aprobadas
- **THEN** el sistema cambia el estado a Aprobada
- **AND** registra administrador, fecha/hora de decisión
- **AND** bloquea ese intervalo para futuras aprobaciones conflictivas

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
El sistema SHALL permitir la cancelación de solicitudes en estados permitidos, conservando el historial con trazabilidad completa.

#### Scenario: Cancelar solicitud propia pendiente
- **WHEN** un Solicitante cancela su propia solicitud en estado Pendiente
- **THEN** el sistema cambia el estado a Cancelada
- **AND** registra fecha/hora de cancelación y usuario que cancela
- **AND** conserva el registro en el historial

#### Scenario: Cancelar reserva aprobada solo con autorización administrativa
- **WHEN** un Administrador autoriza y cancela una solicitud ya Aprobada
- **THEN** el sistema cambia el estado a Cancelada
- **AND** registra administrador autorizante, fecha/hora de cancelación y motivo
- **AND** libera el intervalo
- **AND** conserva el registro en el historial

#### Scenario: No cancelar solicitud ajena como solicitante
- **WHEN** un Solicitante intenta cancelar una solicitud de otro usuario
- **THEN** el sistema deniega la acción
- **AND** no modifica el estado

#### Scenario: No cancelar reserva aprobada como solicitante
- **WHEN** un Solicitante intenta cancelar una solicitud ya Aprobada
- **THEN** el sistema deniega la cancelación
- **AND** informa que solo puede cancelarse con autorización administrativa
- **AND** conserva el registro en el historial

#### Scenario: Consultar historial con filtros
- **WHEN** un usuario consulta su historial de reservas
- **THEN** el sistema muestra solicitudes con estados, fechas, espacio, usuario, decisor/autorizante y detalles
- **AND** permite filtrar por estado, fecha o espacio
- **AND** conserva trazabilidad completa

#### Scenario: Historial completo para administrador
- **WHEN** un Administrador consulta el historial general
- **THEN** el sistema muestra todas las solicitudes con solicitante, administrador decisor/autorizante, fechas, motivos y trazabilidad completa
