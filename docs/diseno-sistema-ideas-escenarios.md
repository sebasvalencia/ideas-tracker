# Escenarios del Sistema Ideas Tracker

## 1. Objetivo

Definir escenarios funcionales y tecnicos para guiar:
- Desarrollo orientado a comportamiento (BDD).
- Pruebas unitarias/integracion/E2E.
- Criterios de validacion de negocio y operacion.

Este documento usa formato Gherkin para facilitar automatizacion con `pytest-bdd` y trazabilidad con tickets del backlog.

---

## 2. Convenciones de escenarios

- Cada feature incluye:
  - objetivo funcional.
  - escenarios felices y escenarios de error.
- Etiquetas sugeridas:
  - `@mvp`, `@auth`, `@ideas`, `@logs`, `@ratings`, `@security`, `@api`, `@ui`, `@e2e`.
- Formato de IDs:
  - `SCN-AUTH-001`, `SCN-IDEA-001`, etc.

---

## 3. Escenarios BDD (Gherkin)

## Feature: Autenticacion y autorizacion

```gherkin
@mvp @auth @api
Feature: Login con OAuth2 y JWT
  Como usuario registrado
  Quiero autenticarme
  Para usar los endpoints protegidos

  @SCN-AUTH-001
  Scenario: Login exitoso con credenciales validas
    Given existe un usuario activo con email "user@test.com" y password valida
    When envio una solicitud POST "/api/v1/auth/login" con sus credenciales
    Then recibo status 200
    And la respuesta contiene "access_token"
    And la respuesta contiene "token_type" con valor "bearer"

  @SCN-AUTH-002
  Scenario: Login fallido con password incorrecta
    Given existe un usuario activo con email "user@test.com"
    When envio una solicitud POST "/api/v1/auth/login" con password incorrecta
    Then recibo status 401
    And la respuesta contiene mensaje de credenciales invalidas

  @SCN-AUTH-003
  Scenario: Acceso denegado a endpoint protegido sin token
    Given no estoy autenticado
    When envio una solicitud GET "/api/v1/ideas"
    Then recibo status 401

  @SCN-AUTH-004
  Scenario: Acceso denegado con token expirado
    Given tengo un token JWT expirado
    When envio una solicitud GET "/api/v1/ideas" con ese token
    Then recibo status 401
    And la respuesta indica token invalido o expirado

  @SCN-AUTH-005
  Scenario: Usuario sin permisos suficientes
    Given estoy autenticado con rol "user"
    And existe un endpoint restringido a rol "admin"
    When accedo al endpoint restringido
    Then recibo status 403
```

## Feature: CRUD de ideas

```gherkin
@mvp @ideas @api
Feature: Gestion de ideas
  Como usuario autenticado
  Quiero crear, consultar, editar y eliminar ideas
  Para gestionar mi portafolio de proyectos

  @SCN-IDEA-001
  Scenario: Crear una idea con datos validos
    Given estoy autenticado
    When envio POST "/api/v1/ideas" con titulo y descripcion validos
    Then recibo status 201
    And la idea queda en estado "idea"
    And el porcentaje de ejecucion inicial es 0

  @SCN-IDEA-002
  Scenario: Fallo al crear idea por titulo vacio
    Given estoy autenticado
    When envio POST "/api/v1/ideas" con titulo vacio
    Then recibo status 422

  @SCN-IDEA-003
  Scenario: Listar ideas del usuario autenticado
    Given estoy autenticado
    And existen ideas creadas por mi usuario
    When envio GET "/api/v1/ideas"
    Then recibo status 200
    And obtengo solo ideas visibles de mi alcance

  @SCN-IDEA-004
  Scenario: Consultar detalle de una idea existente
    Given estoy autenticado
    And existe la idea con id "1001"
    When envio GET "/api/v1/ideas/1001"
    Then recibo status 200
    And la respuesta contiene id "1001"

  @SCN-IDEA-005
  Scenario: No acceder a idea inexistente
    Given estoy autenticado
    When envio GET "/api/v1/ideas/999999"
    Then recibo status 404

  @SCN-IDEA-006
  Scenario: Eliminar idea con borrado logico
    Given estoy autenticado
    And existe la idea con id "1002"
    When envio DELETE "/api/v1/ideas/1002"
    Then recibo status 204
    And la idea no aparece en listados activos
```

## Feature: Estado y porcentaje de ejecucion

```gherkin
@mvp @ideas @api
Feature: Reglas de estado y progreso
  Como usuario autenticado
  Quiero actualizar el estado y porcentaje
  Para reflejar avance real del proyecto

  @SCN-PROG-001
  Scenario: Actualizar porcentaje dentro de rango permitido
    Given estoy autenticado
    And existe una idea en estado "in_progress" con 20 de ejecucion
    When actualizo la idea a 45 de ejecucion
    Then recibo status 200
    And la idea queda con 45 de ejecucion

  @SCN-PROG-002
  Scenario: Rechazar porcentaje mayor a 100
    Given estoy autenticado
    And existe una idea en estado "in_progress"
    When intento actualizar la idea con porcentaje 120
    Then recibo status 422

  @SCN-PROG-003
  Scenario: Marcar idea como terminada con porcentaje 100
    Given estoy autenticado
    And existe una idea en estado "in_progress" con 90 de ejecucion
    When actualizo estado a "terminada" y porcentaje a 100
    Then recibo status 200
    And la idea queda en estado "terminada"

  @SCN-PROG-004
  Scenario: Rechazar estado terminada si porcentaje no es 100
    Given estoy autenticado
    And existe una idea en estado "in_progress" con 80 de ejecucion
    When actualizo estado a "terminada" y porcentaje a 80
    Then recibo status 400
    And la respuesta indica regla de negocio incumplida
```

## Feature: Historial de comentarios y traza

```gherkin
@mvp @logs @api
Feature: Registro de progreso historico
  Como usuario autenticado
  Quiero registrar comentarios de avance
  Para mantener una traza del proyecto

  @SCN-LOG-001
  Scenario: Agregar comentario de avance
    Given estoy autenticado
    And existe una idea con id "2001"
    When envio POST "/api/v1/ideas/2001/logs" con comentario no vacio
    Then recibo status 201
    And el log queda asociado a la idea "2001"

  @SCN-LOG-002
  Scenario: Validar que no se acepten comentarios vacios
    Given estoy autenticado
    And existe una idea con id "2001"
    When envio POST "/api/v1/ideas/2001/logs" con comentario vacio
    Then recibo status 422

  @SCN-LOG-003
  Scenario: Consultar timeline de logs
    Given estoy autenticado
    And existe una idea con id "2001" con multiples logs
    When envio GET "/api/v1/ideas/2001/logs"
    Then recibo status 200
    And obtengo los logs ordenados por fecha descendente

  @SCN-LOG-004
  Scenario: Generar log automatico al cambiar estado o progreso
    Given estoy autenticado
    And existe una idea con id "2002"
    When actualizo su estado o porcentaje
    Then se crea automaticamente un log de sistema
```

## Feature: Calificacion final del proyecto

```gherkin
@mvp @ratings @api
Feature: Rating de cierre de idea
  Como usuario autenticado
  Quiero calificar el resultado final de una idea
  Para medir satisfaccion y aprendizaje

  @SCN-RATE-001
  Scenario: Registrar rating para idea terminada
    Given estoy autenticado
    And existe una idea en estado "terminada"
    When envio POST "/api/v1/ideas/{id}/rating" con valor 8
    Then recibo status 201
    And la idea queda con rating 8

  @SCN-RATE-002
  Scenario: Rechazar rating para idea no terminada
    Given estoy autenticado
    And existe una idea en estado "in_progress"
    When intento registrar rating 8
    Then recibo status 400
    And la respuesta indica que solo aplica a ideas terminadas

  @SCN-RATE-003
  Scenario: Rechazar rating fuera de rango
    Given estoy autenticado
    And existe una idea en estado "terminada"
    When intento registrar rating 15
    Then recibo status 422

  @SCN-RATE-004
  Scenario: Actualizar rating existente
    Given estoy autenticado
    And existe una idea terminada con rating 6
    When actualizo el rating a 9
    Then recibo status 200
    And la idea queda con rating 9
```

## Feature: Frontend - flujo funcional principal

```gherkin
@ui @e2e @mvp
Feature: Flujo de usuario de punta a punta
  Como usuario final
  Quiero gestionar una idea completa desde la UI
  Para validar el valor del sistema

  @SCN-E2E-001
  Scenario: Login, crear idea y ver en listado
    Given abro la aplicacion web en la pagina de login
    When inicio sesion con credenciales validas
    And creo una idea con titulo y descripcion
    Then veo la idea en el listado principal

  @SCN-E2E-002
  Scenario: Actualizar progreso y estado desde detalle
    Given estoy logueado y en el detalle de una idea
    When actualizo progreso a 60 y estado "in_progress"
    Then visualizo el badge de estado actualizado
    And visualizo la barra de progreso en 60

  @SCN-E2E-003
  Scenario: Registrar comentario y visualizar timeline
    Given estoy en el detalle de una idea
    When escribo un comentario en el textarea y lo guardo
    Then veo el comentario en la timeline con fecha reciente

  @SCN-E2E-004
  Scenario: Finalizar y calificar idea
    Given estoy en el detalle de una idea con avance 90
    When actualizo a estado "terminada" y progreso 100
    And envio rating final 10
    Then se muestra la calificacion final en pantalla
```

## Feature: Seguridad y hardening

```gherkin
@security @api
Feature: Reglas de seguridad aplicadas
  Como equipo tecnico
  Quiero proteger autenticacion y endpoints
  Para reducir riesgos operativos

  @SCN-SEC-001
  Scenario: Rechazar JWT firmado con clave invalida
    Given tengo un token alterado manualmente
    When consumo un endpoint protegido
    Then recibo status 401

  @SCN-SEC-002
  Scenario: Aplicar rate limiting en login
    Given intento autenticaciones fallidas repetidas
    When supero el limite permitido por ventana de tiempo
    Then recibo status 429

  @SCN-SEC-003
  Scenario: Rechazar solicitud sin cabecera Authorization
    Given no envio cabecera Authorization
    When consumo endpoint protegido
    Then recibo status 401
```

## Feature: Observabilidad minima

```gherkin
@ops @observability
Feature: Trazas, metricas y logs
  Como equipo de operacion
  Quiero observabilidad del sistema
  Para diagnosticar incidentes y medir salud

  @SCN-OBS-001
  Scenario: Exponer endpoint de metricas
    Given la API esta levantada
    When consulto "/metrics"
    Then recibo status 200
    And obtengo metricas Prometheus parseables

  @SCN-OBS-002
  Scenario: Trazar una solicitud de extremo a extremo
    Given OpenTelemetry esta habilitado
    When ejecuto una solicitud de API
    Then se genera un trace con spans de API y base de datos

  @SCN-OBS-003
  Scenario: Registrar errores en logs estructurados
    Given ocurre una excepcion controlada en la API
    When se genera la respuesta de error
    Then se registra log estructurado con correlacion de trace_id
```

---

## 4. Matriz de cobertura recomendada

| Escenario | Unit | Integracion API | E2E Playwright | Prioridad |
|---|---|---|---|---|
| SCN-AUTH-001 a 005 | Parcial | Si | Si (login base) | P0 |
| SCN-IDEA-001 a 006 | Parcial | Si | Si | P0 |
| SCN-PROG-001 a 004 | Si | Si | Si | P0 |
| SCN-LOG-001 a 004 | Parcial | Si | Si | P0 |
| SCN-RATE-001 a 004 | Si | Si | Si | P1 |
| SCN-SEC-001 a 003 | Parcial | Si | No | P1 |
| SCN-OBS-001 a 003 | No | Si | No | P2 |

---

## 5. Orden de automatizacion sugerido

1. Auth basico (`SCN-AUTH-001/002/003`).
2. CRUD minimo ideas (`SCN-IDEA-001/003/004`).
3. Reglas de progreso/estado (`SCN-PROG-001..004`).
4. Logs de traza (`SCN-LOG-001/003/004`).
5. Rating final (`SCN-RATE-001/002`).
6. Flujo E2E principal (`SCN-E2E-001..004`).
7. Seguridad avanzada y observabilidad (`SCN-SEC-*`, `SCN-OBS-*`).

---

## 6. Criterios para considerar cobertura completa del MVP

- Todos los escenarios `@mvp` implementados y en verde.
- Los escenarios de error critico (auth, validaciones, reglas de negocio) automatizados.
- El flujo E2E principal completo estable en CI.
- Trazabilidad entre escenario <-> ticket del backlog <-> pruebas implementadas.
