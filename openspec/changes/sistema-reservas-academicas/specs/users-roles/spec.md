# Spec Delta

## Purpose

Gestionar el registro de usuarios, autenticación y el sistema de roles y permisos (Administrador y Solicitante) para controlar el acceso a las funcionalidades del sistema.

## ADDED Requirements

### Requirement: Registro y autenticación de usuarios
El sistema SHALL permitir el registro de nuevos usuarios con datos válidos y autenticación mediante credenciales seguras.

#### Scenario: Registro exitoso
- **WHEN** un usuario proporciona datos válidos para registro
- **THEN** el sistema crea la cuenta con rol Solicitante por defecto
- **AND** el usuario puede autenticarse con sus credenciales

#### Scenario: Autenticación exitosa
- **WHEN** un usuario proporciona credenciales correctas
- **THEN** el sistema autentica al usuario
- **AND** establece sesión con su rol correspondiente

#### Scenario: Autenticación fallida
- **WHEN** un usuario proporciona credenciales incorrectas
- **THEN** el sistema rechaza la autenticación
- **AND** no revela información específica sobre qué campo es incorrecto

### Requirement: Gestión de roles y permisos
El sistema SHALL aplicar control de acceso basado en roles, diferenciando permisos entre Administrador y Solicitante.

#### Scenario: Acceso a funciones administrativas
- **WHEN** un usuario con rol Solicitante intenta acceder a funciones administrativas
- **THEN** el sistema deniega el acceso
- **AND** muestra mensaje de autorización denegada

#### Scenario: Acceso a funciones de solicitante
- **WHEN** un usuario con rol Solicitante accede a sus propias funcionalidades
- **THEN** el sistema permite el acceso según sus permisos

#### Scenario: Promoción a Administrador
- **WHEN** un Administrador actualiza el rol de otro usuario a Administrador
- **THEN** el sistema actualiza los permisos
- **AND** registra la acción en bitácora (quién y cuándo)

### Requirement: Administración de usuarios
El sistema SHALL permitir al Administrador listar, consultar, activar/desactivar usuarios y gestionar sus roles.

#### Scenario: Desactivar usuario
- **WHEN** el Administrador desactiva una cuenta de usuario
- **THEN** el sistema impide nuevas autenticaciones
- **AND** no elimina el historial de reservas asociado al usuario
- **AND** registra la acción

#### Scenario: Listado de usuarios con filtros
- **WHEN** el Administrador filtra usuarios por rol o estado
- **THEN** el sistema muestra solo usuarios que coinciden con los filtros
