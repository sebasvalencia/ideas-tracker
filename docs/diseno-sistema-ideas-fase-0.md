# Fase 0 - Descubrimiento y Alineacion (Tickets Detallados)

## 1. Objetivo de la fase

Definir con precision el alcance del MVP, las reglas de negocio, los requerimientos no funcionales y las convenciones de trabajo para iniciar desarrollo con bajo riesgo y alta claridad.

Resultado esperado de la fase:

- Backlog inicial validado.d
- Reglas de negocio acordadas.
- Criterios de calidad/seguridad definidos.
- Convenciones de trabajo listas para ejecutar la Fase 1.

## 1.1 Fuentes base obligatorias (insumo)

Esta Fase 0 se ejecuta usando como fuente de verdad:

- `diseno-sistema-ideas.md` (arquitectura, fases, reglas, stack y estrategia tecnica).
- `diseno-sistema-ideas-escenarios.md` (escenarios BDD/Gherkin y cobertura objetivo).

Regla de trabajo para Fase 0:

- Ningun ticket de Fase 0 se cierra si no deja trazabilidad explicita con al menos una seccion de `diseno-sistema-ideas.md` y un bloque de escenarios de `diseno-sistema-ideas-escenarios.md`.

---

## 2. Orden recomendado de ejecucion (Fase 0)

1. `F0-01` Definir alcance MVP.
2. `F0-02` Acordar reglas de negocio (estado/progreso/rating).
3. `F0-03` Definir NFRs medibles.
4. `F0-04` Definir convenciones de trabajo.
5. `F0-05` Spike gRPC post-MVP (opcional y al final).

---

## 3. Tickets de Fase 0 (detalle paso a paso)

## Ticket F0-01 - Definir alcance MVP

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `3 pts`
- Dependencias: ninguna

### Objetivo

Delimitar exactamente que entra y que no entra al primer release usable.

### Insumos de referencia

- `diseno-sistema-ideas.md`: secciones de requerimientos, stack, fases y roadmap.
- `diseno-sistema-ideas-escenarios.md`: escenarios etiquetados `@mvp`.

### Paso a paso

1. Listar funcionalidades propuestas del documento de diseno.
2. Marcar cada funcionalidad con una etiqueta:
   - `MVP`,
   - `POST-MVP`,
   - `FUTURO`.
3. Redactar alcance funcional de MVP en una pagina:
   - autenticacion,
   - CRUD ideas,
   - estado/progreso,
   - logs,
   - rating.
4. Redactar alcance tecnico MVP:
   - backend FastAPI hexagonal,
   - frontend Next.js modular,
   - Postgres,
   - pruebas minimas,
   - Docker + CI base.
5. Registrar exclusiones explicitas (ejemplo: gRPC y Kubernetes fuera del MVP).
6. Validar y congelar version `MVP v1.0`.

### Entregables

- Documento de alcance MVP.
- Lista de exclusiones y supuestos.
- Version inicial de prioridades funcionales.

### Criterios de aceptacion

- Existe lista clara de `in-scope` y `out-of-scope`.
- No hay ambiguedad en funcionalidades del MVP.
- Se aprueba una version base para iniciar Fase 1.

### Riesgos comunes y mitigacion

- Riesgo: alcance demasiado grande.
  - Mitigacion: aplicar regla "si no es critico para primer flujo, va a post-MVP".

---

## Ticket F0-02 - Acordar reglas de negocio (estado/progreso/rating)

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `3 pts`
- Dependencias: `F0-01`

### Objetivo

Definir reglas de dominio sin ambiguedad para evitar retrabajo en backend y frontend.

### Insumos de referencia

- `diseno-sistema-ideas.md`: reglas funcionales de estado/progreso/logs/rating.
- `diseno-sistema-ideas-escenarios.md`: `SCN-PROG-*`, `SCN-LOG-*`, `SCN-RATE-*`.

### Paso a paso

1. Definir estados oficiales:
   - `idea`,
   - `in_progress`,
   - `terminada`.
2. Definir transiciones permitidas/no permitidas entre estados.
3. Definir reglas del porcentaje:
   - rango 0 a 100,
   - precision permitida (entero o decimal),
   - comportamiento al finalizar.
4. Definir reglas de rating:
   - rango (1-10),
   - solo para ideas `terminada`,
   - si permite edicion posterior o no.
5. Definir reglas de logs:
   - comentario obligatorio o no,
   - log automatico en cambio de estado/progreso.
6. Documentar reglas como tabla de negocio + ejemplos validos/invalidos.

### Entregables

- Matriz de reglas de negocio.
- Tabla de validaciones y errores esperados.
- Casos ejemplo para pruebas unitarias/BDD.

### Criterios de aceptacion

- Todas las reglas clave tienen condicion y resultado esperado.
- Existen ejemplos de borde (ejemplo: porcentaje 100 con estado no terminado).
- Queda lista una base para escenarios Gherkin.

### Riesgos comunes y mitigacion

- Riesgo: reglas contradictorias.
  - Mitigacion: consolidar en una sola tabla versionada y revisada antes de codificar.

---

## Ticket F0-03 - Definir NFRs (seguridad, rendimiento, disponibilidad)

- Tipo: `TASK`
- Prioridad: `P1`
- Estimacion: `2 pts`
- Dependencias: `F0-01`

### Objetivo

Establecer requerimientos no funcionales medibles para guiar decisiones tecnicas.

### Insumos de referencia

- `diseno-sistema-ideas.md`: secciones de seguridad, observabilidad, CI/CD y despliegue.
- `diseno-sistema-ideas-escenarios.md`: `SCN-SEC-*`, `SCN-OBS-*`.

### Paso a paso

1. Definir NFRs de seguridad minimos:
   - JWT con expiracion,
   - hash de password,
   - endpoints protegidos,
   - manejo de secretos por entorno.
2. Definir NFRs de rendimiento inicial:
   - latencia objetivo (p95),
   - tiempo de respuesta maximo para endpoints criticos.
3. Definir NFRs de disponibilidad:
   - uptime objetivo para MVP,
   - recuperacion basica ante caida.
4. Definir NFRs de calidad:
   - cobertura minima backend,
   - gates de CI.
5. Definir NFRs de observabilidad:
   - logs estructurados,
   - metricas minimas.
6. Publicar tabla NFR con metrica y forma de medicion.

### Entregables

- Tabla NFR (requisito, metrica, objetivo, metodo de medicion).
- Criterios de calidad para CI.

### Criterios de aceptacion

- Cada NFR tiene metrica objetiva.
- Existe valor objetivo y mecanismo de verificacion.
- Los NFRs pueden convertirse en checks del pipeline.

### Riesgos comunes y mitigacion

- Riesgo: NFRs "bonitos" pero no medibles.
  - Mitigacion: toda condicion debe incluir numero y test/check asociado.

---

## Ticket F0-04 - Definir convenciones de ramas, commits y versionado API

- Tipo: `TASK`
- Prioridad: `P1`
- Estimacion: `2 pts`
- Dependencias: ninguna

### Objetivo

Estandarizar la forma de trabajo para mantener trazabilidad y consistencia desde el inicio.

### Insumos de referencia

- `diseno-sistema-ideas.md`: diseno API v1, fases y estrategia de pruebas.
- `diseno-sistema-ideas-escenarios.md`: convenciones de IDs `SCN-*` y matriz de cobertura.

### Paso a paso

1. Definir estrategia de ramas:
   - `main` protegida,
   - ramas por ticket (`feature/F4-01-*`, `fix/*`).
2. Definir convencion de commits:
   - formato sugerido (`feat:`, `fix:`, `test:`, `docs:`).
3. Definir reglas de Pull Request:
   - checklist minima,
   - pruebas obligatorias,
   - criterio de aprobacion.
4. Definir versionado de API:
   - base path `/api/v1`,
   - politica de cambios breaking.
5. Definir convención de nombres:
   - tickets,
   - features,
   - escenarios `SCN-*`.
6. Consolidar todo en guia corta de contribucion.

### Entregables

- Guia de contribucion (`workflow` tecnico).
- Norma de versionado API v1.
- Checklist de PR.

### Criterios de aceptacion

- Cualquier ticket puede abrirse con naming estandar.
- El versionado de API queda definido antes de implementar endpoints.
- Existe checklist reutilizable para PR.

### Riesgos comunes y mitigacion

- Riesgo: desorden de ramas/commits.
  - Mitigacion: forzar plantilla simple de PR y convención de branch por ticket.

---

## Ticket F0-05 - Spike gRPC post-MVP

- Tipo: `SPIKE`
- Prioridad: `P3`
- Estimacion: `2 pts`
- Dependencias: `F0-01`

### Objetivo

Evaluar si gRPC aporta valor real para una fase posterior sin bloquear el MVP.

### Insumos de referencia

- `diseno-sistema-ideas.md`: stack tecnico, roadmap y riesgo de sobre-complejidad temprana.
- `diseno-sistema-ideas-escenarios.md`: alcance centrado en REST para MVP.

### Paso a paso

1. Identificar casos candidatos para gRPC (si existen):
   - alto throughput,
   - contratos internos entre servicios.
2. Comparar REST vs gRPC para este proyecto en 1 pagina:
   - complejidad,
   - tooling,
   - impacto en frontend web.
3. Definir criterio de decision:
   - "adoptar despues de MVP" o "no aplicar por ahora".
4. Registrar decision final y fecha de reevaluacion.

### Entregables

- Nota tecnica del spike (con decision explicita).

### Criterios de aceptacion

- Existe decision documentada.
- No genera impacto en cronograma de MVP.

### Riesgos comunes y mitigacion

- Riesgo: sobre-disenar temprano.
  - Mitigacion: mantener gRPC como experimento no bloqueante.

---

## 4. Checklist de cierre de Fase 0

- `F0-01` completado y aprobado.
- `F0-02` completado y aprobado.
- `F0-03` completado y aprobado.
- `F0-04` completado y aprobado.
- `F0-05` resuelto o explicitamente diferido.
- Backlog listo para iniciar Fase 1.
- Escenarios BDD alineados con reglas de negocio.

---

## 4.1 Matriz de trazabilidad Fase 0 (fuente -> salida)

| Ticket Fase 0 | Secciones fuente (`diseno-sistema-ideas.md`) | Escenarios fuente (`diseno-sistema-ideas-escenarios.md`) | Salida obligatoria |
|---|---|---|---|
| F0-01 | Vision, requerimientos funcionales, fases, roadmap | `@mvp` (`SCN-AUTH-*`, `SCN-IDEA-*`, `SCN-PROG-*`, `SCN-LOG-*`, `SCN-RATE-*`, `SCN-E2E-*`) | Lista `in-scope`/`out-of-scope` validada |
| F0-02 | Reglas de negocio, modelo de datos, API REST | `SCN-PROG-*`, `SCN-LOG-*`, `SCN-RATE-*` | Matriz de reglas de dominio + casos borde |
| F0-03 | Seguridad, observabilidad, calidad, CI/CD | `SCN-SEC-*`, `SCN-OBS-*` | Tabla NFR medible con umbrales |
| F0-04 | API v1, estrategia de pruebas y fases | Convenciones `SCN-*`, cobertura recomendada | Workflow de ramas/PR/commits + politica API |
| F0-05 | Stack y plan por fases (REST primero) | Alcance de escenarios REST/E2E MVP | Decision documentada de gRPC post-MVP |

Regla de aprobacion:

- Cada ticket debe adjuntar evidencia de trazabilidad (seccion fuente + escenarios impactados + artefacto generado).

---

## 5. Definition of Done (DoD) de la Fase 0

La Fase 0 se considera cerrada cuando:

- El alcance MVP esta congelado y versionado.
- Las reglas de negocio estan completas y sin contradicciones.
- NFRs estan definidos con metricas medibles.
- Convenciones de desarrollo y API quedaron documentadas.
- Existe trazabilidad entre alcance, backlog y escenarios.

---

## 6. Siguiente paso inmediato recomendado

Iniciar Fase 1 con los tickets `F1-01`, `F1-02` y `F1-03` en paralelo corto, manteniendo `WIP = 1` por ticket para asegurar finalizacion y no dispersion.

---

## 7. Decisiones aprobadas (resultado de seleccion)

Estas decisiones quedan congeladas para cerrar Fase 0:

- Alcance MVP: `amplio`.
- gRPC en MVP: `no` (se difiere).
- Modelo auth inicial: `usuarios locales + JWT`.
- Escala de rating: `1..10`.
- Precision de progreso: `decimal(5,2)`.
- Transicion de estados: `flexible` con validaciones de negocio.
- Latencia objetivo p95: `<= 500 ms`.
- Cobertura minima backend CI: `>= 80%`.
- Estrategia de ramas: `hibrida` (`main + feature/* + release/*`).
- Convencion de commits: `Conventional Commits + prefijo de ticket` (ej: `feat(F4-01): ...`).
- Observabilidad MVP: `completa` (metricas + trazas + dashboards + alertas iniciales).
- Contenerizacion MVP: `Docker API + Web + Postgres + Prometheus + Grafana`.
- Disponibilidad objetivo MVP: `99.5%`.
- RTO objetivo: `30 minutos`.
- Rate limit login: `5 intentos/min por IP/usuario`.
- Politica de logs: `manual + automatico por cambio de estado/progreso`.
- Politica breaking API: `solo en nueva version` (`/api/v2`).
- Checks obligatorios de PR: `tests`, `coverage`, `lint`, `docs`, `SCN vinculados`.
- Re-evaluacion gRPC: `al cerrar Fase 8`.

---

## 8. Productos finales por ticket (Fase 0)

## F0-01 - Producto final: Acta de alcance MVP v1.0

### Alcance funcional IN

- Login con usuarios locales (`email/password`) + JWT.
- CRUD de ideas.
- Estado y porcentaje de ejecucion con reglas validadas.
- Logs de progreso manuales.
- Logs automaticos en cambios de estado/progreso.
- Rating final (`1..10`) para ideas terminadas.
- Frontend Next.js modular para flujo principal.

### Alcance tecnico IN

- Backend FastAPI con base hexagonal.
- SQLAlchemy + Alembic + Postgres.
- Pruebas unitarias + BDD + E2E.
- Docker Compose con `api`, `web`, `postgres`, `prometheus`, `grafana`.
- CI base con quality gates.

### Alcance OUT (post-MVP)

- gRPC (solo documentacion/decision).
- Kubernetes productivo completo.
- Estrategias avanzadas de despliegue (canary/blue-green) en produccion real.

### Criterio de cierre F0-01

- Documento de alcance versionado y aprobado.

---

## F0-02 - Producto final: Matriz de reglas de negocio

### Reglas de estado/progreso

- Estados permitidos: `idea`, `in_progress`, `terminada`.
- Transiciones: flexibles, pero siempre validadas.
- `execution_percentage` en `0..100` con precision `2 decimales`.
- Si estado `terminada` entonces progreso debe ser `100`.

### Reglas de logs/traza

- Log manual permitido para seguimiento.
- Log automatico obligatorio al cambiar estado/progreso.
- Cada log guarda snapshot de estado y progreso.

### Reglas de rating

- Rango `1..10`.
- Solo permitido en ideas `terminada`.
- Puede actualizarse segun politica de negocio del endpoint PATCH.

### Criterio de cierre F0-02

- Tabla de reglas y casos borde publicada y trazada a `SCN-PROG-*`, `SCN-LOG-*`, `SCN-RATE-*`.

---

## F0-03 - Producto final: Baseline de NFRs medibles

| Categoria | NFR | Objetivo aprobado | Verificacion |
|---|---|---|---|
| Rendimiento | Latencia p95 endpoints criticos | <= 500 ms | Metricas Prometheus |
| Disponibilidad | Uptime MVP | 99.5% | Monitoreo + registros de incidentes |
| Recuperacion | RTO | 30 min | Simulacro/ejercicio de recuperacion |
| Seguridad | Rate limit login | 5/min IP/usuario | Pruebas de integracion (`429`) |
| Calidad | Cobertura backend | >= 80% | Gate CI pytest-cov |
| Observabilidad | Trazas/metricas/logs | Habilitado en MVP | Dashboards + alertas |

### Criterio de cierre F0-03

- NFRs versionados y convertibles a checks tecnicos.

---

## F0-04 - Producto final: Convenciones de trabajo y API

### Branching

- `main`: estable/protegida.
- `feature/<ticket>-<descripcion-corta>`.
- `release/<version>` para consolidacion.

### Commits

- Formato obligatorio: `tipo(ticket): mensaje`.
- Ejemplos:
  - `feat(F4-01): create idea endpoint`
  - `fix(F3-01): reject invalid jwt signature`
  - `test(F6-03): add bdd auth scenarios`

### Pull Request - checks obligatorios

- Tests en verde.
- Cobertura minima alcanzada.
- Lint/formato en verde.
- Documentacion actualizada si aplica.
- Escenarios `SCN-*` vinculados.

### API versioning

- Version activa inicial: `/api/v1`.
- Breaking changes solo en nueva version (`/api/v2`).

### Criterio de cierre F0-04

- Guia de contribucion publicada y aplicada en primeros PRs.

---

## F0-05 - Producto final: Decision gRPC post-MVP

### Decision

- gRPC no entra en MVP.
- Mantener REST como interfaz principal.
- Re-evaluar gRPC al cerrar Fase 8.

### Condiciones para adoptar gRPC despues

- Necesidad real de comunicacion interna de alto throughput.
- Multiples servicios internos que se beneficien de contratos fuertemente tipados.
- Capacidad operativa para soportar complejidad adicional.

### Criterio de cierre F0-05

- Nota tecnica de decision publicada en `docs/decisions`.

---

## 9. Checklist final de aprobacion de Fase 0

- [ ] F0-01 aprobado con alcance MVP v1.0.
- [ ] F0-02 aprobado con matriz de reglas.
- [ ] F0-03 aprobado con NFRs medibles.
- [ ] F0-04 aprobado con workflow y API versioning.
- [ ] F0-05 aprobado con decision gRPC diferida.
- [ ] Trazabilidad verificada con backlog y escenarios.
