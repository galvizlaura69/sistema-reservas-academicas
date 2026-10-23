# Spec Delta

## Purpose

Permitir la gestión centralizada de espacios académicos (laboratorios, auditorios y salas de cómputo) con su registro, atributos, estado y consulta de disponibilidad.

## ADDED Requirements

### Requirement: Registrar espacios académicos
El sistema SHALL permitir al Administrador registrar nuevos espacios académicos especificando nombre, tipo (laboratorio/auditorio/sala de cómputo), capacidad, ubicación, estado (activo/inactivo) y descripción opcional.

#### Scenario: Registro exitoso de espacio
- **WHEN** el Administrador proporciona datos válidos para un nuevo espacio
- **THEN** el sistema crea el espacio con estado activo por defecto
- **AND** el espacio queda disponible para consulta y solicitudes de reserva

#### Scenario: Registro con datos inválidos
- **WHEN** el Administrador omite campos obligatorios o proporciona valores inválidos
- **THEN** el sistema rechaza el registro
- **AND** muestra un mensaje de error claro

### Requirement: Consultar espacios disponibles
El sistema SHALL permitir a usuarios autenticados consultar la lista de espacios académicos activos, filtrando por tipo, capacidad o fecha/hora para verificar disponibilidad.

#### Scenario: Consulta sin filtros
- **WHEN** un usuario autenticado solicita la lista de espacios
- **THEN** el sistema muestra solo espacios con estado activo
- **AND** presenta información básica de cada espacio

#### Scenario: Consulta con filtro por disponibilidad
- **WHEN** un usuario filtra espacios para una fecha y horario específicos
- **THEN** el sistema indica el estado de disponibilidad de cada espacio en ese intervalo
- **AND** solo muestra espacios que pueden recibir solicitudes en ese contexto

### Requirement: Administrar espacios académicos
El sistema SHALL permitir al Administrador editar, activar/desactivar o eliminar espacios académicos, manteniendo trazabilidad de las acciones.

#### Scenario: Desactivar espacio con reservas futuras aprobadas
- **WHEN** el Administrador intenta desactivar un espacio que tiene reservas aprobadas futuras
- **THEN** el sistema SHALL impedir la desactivación
- **AND** informar al Administrador que debe resolver esas reservas aprobadas primero
- **AND** no eliminar automáticamente las reservas aprobadas existentes

#### Scenario: Editar atributos de espacio
- **WHEN** el Administrador actualiza atributos válidos de un espacio
- **THEN** el sistema guarda los cambios
- **AND** los cambios se reflejan en consultas futuras
