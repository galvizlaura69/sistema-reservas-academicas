# Proposal

## Why

La universidad necesita centralizar las reservas de laboratorios, auditorios y salas de cómputo. Actualmente existen dificultades para consultar disponibilidad, hay solicitudes duplicadas, conflictos de horarios y se carece de un proceso claro para aprobación/rechazo de solicitudes. Esto genera ineficiencia operativa y frustración entre los usuarios. Es necesario contar con un sistema web académico que estandarice el proceso de reservas.

## What Changes

Se desarrollará un sistema web de gestión de reservas de espacios académicos con las siguientes funcionalidades:

- **Gestión de espacios académicos**: Registro, consulta y administración de espacios (laboratorios, auditorios, salas de cómputo) con sus características y disponibilidad.
- **Registro y administración de usuarios**: Sistema de registro de usuarios con perfiles diferenciados.
- **Roles y permisos**: Dos roles principales: Administrador (gestiona espacios, aprueba/rechaza solicitudes, gestiona usuarios) y Solicitante (crea solicitudes, consulta disponibilidad, cancela sus propias solicitudes).
- **Creación de solicitudes de reserva**: Los solicitantes podrán crear solicitudes especificando espacio, fecha, hora de inicio y fin.
- **Consulta y validación de disponibilidad**: El sistema debe validar que un espacio esté disponible en el horario solicitado.
- **Prevención de reservas superpuestas y simultáneas**: Debe impedir crear solicitudes que se solapen con reservas ya aprobadas o en proceso de validación, y proteger contra reservas simultáneas (condición de carrera).
- **Aprobación y rechazo de solicitudes**: Los administradores podrán aprobar o rechazar solicitudes, dejando registro de quién y cuándo lo hizo.
- **Cancelación e historial de reservas**: Los solicitantes podrán cancelar sus propias solicitudes (en estados permitidos), y tanto usuarios como administradores tendrán acceso al historial de reservas con filtros.

**Nota**: Se incorpora la restricción futura de "máximo cuatro horas consecutivas" la cual será gestionada como un cambio formal mediante OpenSpec, no como parte de esta propuesta inicial.

## Capabilities

### New Capabilities

- `spaces`: Gestión de espacios académicos (laboratorios, auditorios, salas de cómputo), sus atributos, estado y disponibilidad.
- `users-roles`: Registro de usuarios, autenticación y gestión de roles (Administrador/Solicitante) con sus permisos.
- `reservations`: Creación, validación de disponibilidad, prevención de solapamientos, aprobación/rechazo, cancelación e historial de solicitudes de reserva.

### Modified Capabilities

Ninguna.

## Impact

**Código afectado**: Nueva aplicación web Flask con arquitectura modular (modelos, vistas/controladores, servicios, plantillas, tests).

**Tecnologías**: Python, Flask, SQLite, HTML/CSS, pytest para pruebas automatizadas.

**APIs/Sistemas**: Endpoints para gestión de espacios, usuarios, autenticación y reservas.

**Base de datos**: Esquema SQLite con tablas para espacios, usuarios, roles, solicitudes/reservas, logs de auditoría.

**Seguridad**: Control de acceso basado en roles, validación de datos, protección contra reservas simultáneas (transacciones/concurrencia).

**Integración**: Sin integraciones externas en esta fase.
