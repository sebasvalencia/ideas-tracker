# Backlog del Sistema Ideas Tracker

## 1. Objetivo del backlog

Este backlog traduce las fases del documento de diseno en tickets ejecutables, revisables y priorizados para implementacion incremental del producto.

Convenciones usadas:

- Prioridad: `P0` (critico), `P1` (alto), `P2` (medio), `P3` (bajo).
- Tipo: `EPIC`, `STORY`, `TASK`, `SPIKE`, `BUG`.
- Estado sugerido: `TODO`, `IN_PROGRESS`, `REVIEW`, `DONE`.
- Estimacion sugerida: escala simple en puntos (`1, 2, 3, 5, 8, 13`).

---

## 2. Roadmap por fases (ordenado)

- Fase 0: Descubrimiento y alineacion.
- Fase 1: Base de arquitectura y repositorio.
- Fase 2: Modelo de datos y persistencia.
- Fase 3: Seguridad y autenticacion.
- Fase 4: API de dominio (ideas, logs, rating).
- Fase 5: Frontend en Next.js por modulos/features.
- Fase 6: Calidad, BDD y pruebas.
- Fase 7: Observabilidad.
- Fase 8: Contenerizacion y despliegue inicial.
- Fase 9: Kubernetes y hardening productivo.

---

## 3. Tickets por fase

## Fase 0 - Descubrimiento y alineacion

### EPIC F0-E1 - Definicion funcional del MVP


| ID    | Tipo  | Titulo                                                  | Prioridad | Est. | Dependencias | Criterios de aceptacion                                       |
| ----- | ----- | ------------------------------------------------------- | --------- | ---- | ------------ | ------------------------------------------------------------- |
| F0-01 | STORY | Definir alcance MVP                                     | P0        | 3    | -            | Existe lista de funcionalidades incluidas/excluidas del MVP   |
| F0-02 | STORY | Acordar reglas de negocio de estado/progreso/rating     | P0        | 3    | F0-01        | Reglas documentadas y validadas por negocio                   |
| F0-03 | TASK  | Definir NFRs (seguridad, performance, disponibilidad)   | P1        | 2    | F0-01        | NFRs medibles definidos                                       |
| F0-04 | TASK  | Definir convenciones de ramas, commits y versionado API | P1        | 2    | -            | Guia de contribucion documentada                              |
| F0-05 | SPIKE | Evaluar alcance inicial de gRPC (post-MVP)              | P3        | 2    | F0-01        | Decision registrada: no incluir en MVP o incluir uso concreto |


## Fase 1 - Base de arquitectura y repositorio

### EPIC F1-E1 - Inicializacion de plataforma


| ID    | Tipo | Titulo                                                             | Prioridad | Est. | Dependencias | Criterios de aceptacion                        |
| ----- | ---- | ------------------------------------------------------------------ | --------- | ---- | ------------ | ---------------------------------------------- |
| F1-01 | TASK | Crear estructura monorepo (`backend`, `frontend`, `infra`, `docs`) | P0        | 2    | F0-04        | Estructura creada y versionada                 |
| F1-02 | TASK | Bootstrap FastAPI + `uv`                                           | P0        | 3    | F1-01        | API responde healthcheck                       |
| F1-03 | TASK | Bootstrap Next.js (App Router)                                     | P0        | 3    | F1-01        | Frontend levanta en local                      |
| F1-04 | TASK | Definir arquitectura hexagonal base en backend                     | P0        | 5    | F1-02        | Capas y carpetas creadas con ejemplo funcional |
| F1-05 | TASK | Configurar entorno local con variables por entorno                 | P1        | 2    | F1-02, F1-03 | `.env.example` definido y funcionando          |
| F1-06 | TASK | Documentar C4 nivel C1/C2 inicial                                  | P2        | 2    | F1-01        | Diagramas publicados en `docs`                 |


## Fase 2 - Modelo de datos y persistencia

### EPIC F2-E1 - Persistencia y migraciones


| ID    | Tipo  | Titulo                                                       | Prioridad | Est. | Dependencias | Criterios de aceptacion              |
| ----- | ----- | ------------------------------------------------------------ | --------- | ---- | ------------ | ------------------------------------ |
| F2-01 | TASK  | Configurar SQLAlchemy 2.x y session management               | P0        | 3    | F1-04        | Conexion a Postgres operativa        |
| F2-02 | TASK  | Configurar Alembic y estrategia de migraciones               | P0        | 3    | F2-01        | Migracion inicial ejecutable         |
| F2-03 | STORY | Modelar tablas `users`, `roles`, `user_roles`                | P0        | 3    | F2-02        | Tablas creadas con constraints       |
| F2-04 | STORY | Modelar tablas `ideas`, `idea_progress_logs`, `idea_ratings` | P0        | 5    | F2-02        | Tablas creadas con checks de negocio |
| F2-05 | TASK  | Definir indices y claves foraneas de alto impacto            | P1        | 2    | F2-03, F2-04 | Consultas principales optimizadas    |
| F2-06 | TASK  | Crear seeds iniciales (roles, usuario admin)                 | P2        | 2    | F2-03        | Seed ejecutable en local/dev         |


## Fase 3 - Seguridad y autenticacion

### EPIC F3-E1 - Auth OAuth2 + JWT


| ID    | Tipo  | Titulo                                          | Prioridad | Est. | Dependencias | Criterios de aceptacion                 |
| ----- | ----- | ----------------------------------------------- | --------- | ---- | ------------ | --------------------------------------- |
| F3-01 | STORY | Implementar login con OAuth2/JWT                | P0        | 5    | F2-03        | Endpoint `/auth/login` emite JWT valido |
| F3-02 | TASK  | Implementar hash/verify de password             | P0        | 2    | F3-01        | Password nunca se persiste en claro     |
| F3-03 | TASK  | Implementar autorizacion por rol                | P1        | 3    | F3-01        | Endpoints protegidos por roles/scopes   |
| F3-04 | TASK  | Manejo de expiracion y refresh token (opcional) | P2        | 3    | F3-01        | Refresh funcional si se habilita        |
| F3-05 | TASK  | Endurecer seguridad: rate limit login y headers | P1        | 3    | F3-01        | Controles de seguridad activos          |


## Fase 4 - API de dominio (ideas, logs, rating)

### EPIC F4-E1 - Nucleo funcional del negocio


| ID    | Tipo  | Titulo                                                 | Prioridad | Est. | Dependencias | Criterios de aceptacion              |
| ----- | ----- | ------------------------------------------------------ | --------- | ---- | ------------ | ------------------------------------ |
| F4-01 | STORY | Crear idea (`POST /ideas`)                             | P0        | 3    | F3-01, F2-04 | Idea creada asociada al owner        |
| F4-02 | STORY | Listar ideas (`GET /ideas`)                            | P0        | 2    | F4-01        | Listado paginado y filtrable basico  |
| F4-03 | STORY | Ver detalle de idea (`GET /ideas/{id}`)                | P0        | 2    | F4-01        | Retorna detalle correcto y permisos  |
| F4-04 | STORY | Actualizar idea (`PATCH /ideas/{id}`)                  | P0        | 5    | F4-01        | Valida transiciones y porcentaje     |
| F4-05 | STORY | Eliminar idea (soft delete)                            | P1        | 3    | F4-01        | Idea no visible en listados activos  |
| F4-06 | STORY | Crear log de progreso (`POST /ideas/{id}/logs`)        | P0        | 3    | F4-01        | Log persistido con snapshot          |
| F4-07 | STORY | Listar logs de progreso                                | P1        | 2    | F4-06        | Timeline ordenado por fecha          |
| F4-08 | STORY | Crear/editar rating final de idea                      | P1        | 3    | F4-04        | Rating permitido solo si `terminada` |
| F4-09 | TASK  | Registrar log automatico en cambios de estado/progreso | P1        | 3    | F4-04, F4-06 | Todo cambio relevante deja traza     |


## Fase 5 - Frontend por modulos/features

### EPIC F5-E1 - UI funcional del MVP


| ID    | Tipo  | Titulo                                          | Prioridad | Est. | Dependencias | Criterios de aceptacion                |
| ----- | ----- | ----------------------------------------------- | --------- | ---- | ------------ | -------------------------------------- |
| F5-01 | STORY | Feature `auth`: pantalla login y sesion         | P0        | 5    | F3-01        | Usuario inicia sesion y persiste token |
| F5-02 | STORY | Feature `ideas`: listado y crear idea           | P0        | 5    | F4-01, F4-02 | Usuario crea y visualiza ideas         |
| F5-03 | STORY | Feature `ideas`: detalle y actualizacion        | P0        | 5    | F4-03, F4-04 | Usuario actualiza estado/progreso      |
| F5-04 | STORY | Feature `progress-logs`: textarea + timeline    | P0        | 3    | F4-06, F4-07 | Se agregan comentarios y se listan     |
| F5-05 | STORY | Feature `ratings`: registrar calificacion final | P1        | 3    | F4-08        | Se califica idea terminada             |
| F5-06 | TASK  | Manejo global de errores API y estados de carga | P1        | 2    | F5-01        | UX consistente en errores/loading      |
| F5-07 | TASK  | Guard de rutas privadas                         | P1        | 2    | F5-01        | Rutas privadas bloqueadas sin auth     |


## Fase 6 - Calidad, BDD y pruebas

### EPIC F6-E1 - Cobertura y confiabilidad


| ID    | Tipo  | Titulo                                                          | Prioridad | Est. | Dependencias  | Criterios de aceptacion               |
| ----- | ----- | --------------------------------------------------------------- | --------- | ---- | ------------- | ------------------------------------- |
| F6-01 | TASK  | Configurar pytest + cobertura                                   | P0        | 2    | F1-02         | Suite backend ejecuta en CI/local     |
| F6-02 | STORY | Pruebas unitarias de dominio (reglas de estado/progreso/rating) | P0        | 5    | F4-04, F4-08  | Cobertura de reglas criticas >= 90%   |
| F6-03 | STORY | Implementar BDD con `pytest-bdd`                                | P0        | 5    | F4-01 a F4-09 | Features Gherkin ejecutan en pipeline |
| F6-04 | STORY | Configurar Playwright para E2E                                  | P0        | 5    | F5-01 a F5-05 | Flujos criticos pasan end-to-end      |
| F6-05 | TASK  | Configurar quality gate (fallar CI por cobertura minima)        | P1        | 2    | F6-01         | CI falla bajo umbral definido         |


## Fase 7 - Observabilidad

### EPIC F7-E1 - Telemetria tecnica y de negocio


| ID    | Tipo | Titulo                                               | Prioridad | Est. | Dependencias | Criterios de aceptacion                      |
| ----- | ---- | ---------------------------------------------------- | --------- | ---- | ------------ | -------------------------------------------- |
| F7-01 | TASK | Integrar OpenTelemetry en FastAPI                    | P1        | 3    | F1-02        | Trazas visibles en backend de observabilidad |
| F7-02 | TASK | Exponer metricas Prometheus (`/metrics`)             | P1        | 2    | F1-02        | Metricas scrapeables                         |
| F7-03 | TASK | Dashboard Grafana tecnico (API/DB)                   | P2        | 3    | F7-01, F7-02 | Dashboard operativo disponible               |
| F7-04 | TASK | Dashboard negocio (ideas creadas/finalizadas/rating) | P2        | 3    | F4-01, F4-08 | KPIs visibles en Grafana                     |
| F7-05 | TASK | Definir alertas y runbooks iniciales                 | P2        | 2    | F7-03        | Alertas documentadas y activas               |


## Fase 8 - Contenerizacion y despliegue inicial

### EPIC F8-E1 - Entrega continua base


| ID    | Tipo  | Titulo                                                | Prioridad | Est. | Dependencias | Criterios de aceptacion                 |
| ----- | ----- | ----------------------------------------------------- | --------- | ---- | ------------ | --------------------------------------- |
| F8-01 | TASK  | Crear Dockerfile backend                              | P0        | 2    | F1-02        | Imagen backend construye correctamente  |
| F8-02 | TASK  | Crear Dockerfile frontend                             | P0        | 2    | F1-03        | Imagen frontend construye correctamente |
| F8-03 | TASK  | Crear Docker Compose de entorno local completo        | P0        | 3    | F8-01, F8-02 | Stack completo levanta en un comando    |
| F8-04 | STORY | Pipeline GitHub Actions lint + tests backend/frontend | P0        | 5    | F6-01, F6-04 | Pipeline ejecuta y reporta estado       |
| F8-05 | TASK  | Pipeline build y publicacion de imagenes              | P1        | 3    | F8-01, F8-02 | Imagen versionada publicada             |


## Fase 9 - Kubernetes y hardening productivo

### EPIC F9-E1 - Operacion en cluster


| ID    | Tipo | Titulo                                               | Prioridad | Est. | Dependencias | Criterios de aceptacion                  |
| ----- | ---- | ---------------------------------------------------- | --------- | ---- | ------------ | ---------------------------------------- |
| F9-01 | TASK | Definir manifests o Helm charts para API/Web         | P1        | 5    | F8-05        | Despliegue en namespace objetivo         |
| F9-02 | TASK | Configurar Ingress, TLS y secretos                   | P1        | 3    | F9-01        | Servicio accesible por HTTPS             |
| F9-03 | TASK | Configurar probes y autoscaling (HPA)                | P2        | 3    | F9-01        | Pods saludables y escalables             |
| F9-04 | TASK | Configurar estrategia de despliegue (rolling/canary) | P2        | 3    | F9-01        | Deploy sin downtime significativo        |
| F9-05 | TASK | Pruebas de carga y ajuste de recursos                | P2        | 5    | F9-03        | Limites/requests ajustados con evidencia |


---

## 4. Sprint sugerido (ejemplo)

- Sprint 1: F0 + F1 + inicio F2.
- Sprint 2: cierre F2 + F3.
- Sprint 3: F4.
- Sprint 4: F5 + inicio F6.
- Sprint 5: cierre F6 + F7.
- Sprint 6: F8.
- Sprint 7: F9.

---

## 5. Tickets criticos para arrancar (top 15)

1. F0-01 Definir alcance MVP.
2. F0-02 Acordar reglas de negocio.
3. F1-01 Estructura monorepo.
4. F1-02 Bootstrap FastAPI + uv.
5. F1-03 Bootstrap Next.js.
6. F1-04 Base hexagonal backend.
7. F2-01 SQLAlchemy.
8. F2-02 Alembic.
9. F2-04 Modelo de ideas/logs/ratings.
10. F3-01 Login OAuth2/JWT.
11. F4-01 Crear idea.
12. F4-04 Actualizar idea con validaciones.
13. F4-06 Crear logs.
14. F5-01 Login UI.
15. F6-01 Configurar pytest + cobertura.

---

## 6. Definicion de Ready (DoR) para tickets

Un ticket puede entrar a desarrollo cuando:

- Tiene descripcion de negocio clara.
- Tiene criterios de aceptacion verificables.
- Tiene dependencias declaradas.
- Tiene estimacion acordada.
- Tiene alcance acotado a un sprint.

## 7. Definicion de Done (DoD) para tickets

Un ticket se considera cerrado cuando:

- Cumple todos sus criterios de aceptacion.
- Incluye pruebas automatizadas relevantes.
- Pasa pipeline de CI.
- Tiene documentacion actualizada si aplica.
- Fue revisado y aprobado en PR.

---

## 8. Matriz de trazabilidad (ticket -> escenarios)

Referencia de escenarios: `diseno-sistema-ideas-escenarios.md`.

| Ticket | Escenarios asociados | Tipo de prueba principal | Prioridad de validacion |
|---|---|---|---|
| F3-01 | SCN-AUTH-001, SCN-AUTH-002 | Integracion API + Unit auth | P0 |
| F3-03 | SCN-AUTH-005 | Integracion API | P1 |
| F3-05 | SCN-SEC-002, SCN-SEC-003 | Integracion API | P1 |
| F4-01 | SCN-IDEA-001, SCN-E2E-001 | Integracion API + E2E | P0 |
| F4-02 | SCN-IDEA-003 | Integracion API | P0 |
| F4-03 | SCN-IDEA-004, SCN-IDEA-005 | Integracion API | P0 |
| F4-04 | SCN-PROG-001, SCN-PROG-002, SCN-PROG-003, SCN-PROG-004, SCN-E2E-002, SCN-E2E-004 | Unit dominio + Integracion API + E2E | P0 |
| F4-05 | SCN-IDEA-006 | Integracion API | P1 |
| F4-06 | SCN-LOG-001, SCN-LOG-002 | Integracion API | P0 |
| F4-07 | SCN-LOG-003 | Integracion API | P1 |
| F4-08 | SCN-RATE-001, SCN-RATE-002, SCN-RATE-003, SCN-RATE-004, SCN-E2E-004 | Unit dominio + Integracion API + E2E | P1 |
| F4-09 | SCN-LOG-004 | Unit casos de uso + Integracion API | P1 |
| F5-01 | SCN-E2E-001 | E2E Playwright | P0 |
| F5-02 | SCN-E2E-001 | E2E Playwright | P0 |
| F5-03 | SCN-E2E-002 | E2E Playwright | P0 |
| F5-04 | SCN-E2E-003 | E2E Playwright | P0 |
| F5-05 | SCN-E2E-004 | E2E Playwright | P1 |
| F6-02 | SCN-PROG-001..004, SCN-RATE-001..004 | Unit dominio | P0 |
| F6-03 | SCN-AUTH-*, SCN-IDEA-*, SCN-PROG-*, SCN-LOG-*, SCN-RATE-* | BDD (`pytest-bdd`) | P0 |
| F6-04 | SCN-E2E-001..004 | E2E Playwright | P0 |
| F7-01 | SCN-OBS-002 | Integracion tecnica | P2 |
| F7-02 | SCN-OBS-001 | Integracion tecnica | P2 |
| F7-03 | SCN-OBS-003 | Integracion tecnica | P2 |

Notas:
- Los tickets de F0-F2 y F8-F9 son mayormente habilitadores; su validacion se concentra en smoke tests, checks de pipeline y criterios de infraestructura.
- Cuando un ticket referencia rangos (`..` o `*`), se recomienda desglosar en subtareas por escenario al planificar sprint.

