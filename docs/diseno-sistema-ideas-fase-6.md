# Fase 6 - Calidad, BDD y Pruebas (Tickets + Pasos + Comandos)

## 1. Objetivo de la fase

Consolidar la calidad del sistema con una suite automatizada: unitarias, BDD con Gherkin y E2E con Playwright, incluyendo umbrales de cobertura y quality gates en CI.

## 1.1 Fuentes base

- `diseno-sistema-ideas.md`
- `diseno-sistema-ideas-backlog.md`
- `diseno-sistema-ideas-escenarios.md`
- `diseno-sistema-ideas-fase-3.md`
- `diseno-sistema-ideas-fase-4.md`
- `diseno-sistema-ideas-fase-5.md`

---

## 2. Orden de ejecucion recomendado (Fase 6)

1. `F6-01` Configurar pytest + cobertura.
2. `F6-02` Unit tests de dominio.
3. `F6-03` BDD con pytest-bdd.
4. `F6-04` E2E con Playwright.
5. `F6-05` Quality gates.

---

## 3. Estructura de pruebas objetivo

```text
backend/tests/
  unit/
  integration/
  bdd/
    features/
    steps/

frontend/tests/
  e2e/
```

---

## 4. Tickets de Fase 6 (detalle paso a paso)

## Ticket F6-01 - Configurar pytest + cobertura

- Tipo: `TASK`
- Prioridad: `P0`
- Estimacion: `2 pts`
- Dependencias: `F4-*`

### Paso a paso

1. Instalar dependencias de testing backend.
2. Crear `pytest.ini`.
3. Configurar reporte de cobertura.
4. Crear fixtures base de DB/cliente API.

### Comandos (PowerShell)

```powershell
cd backend
uv add --dev pytest pytest-cov pytest-asyncio httpx
New-Item -ItemType File -Path pytest.ini -Force
mkdir tests,tests\unit,tests\integration,tests\bdd,tests\bdd\features,tests\bdd\steps
```

### Criterios de aceptacion

- `pytest` ejecuta sin errores de configuracion.
- Se genera reporte de cobertura.

---

## Ticket F6-02 - Unit tests de dominio y casos de uso

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F6-01`

### Paso a paso

1. Cubrir validaciones de porcentaje y estado.
2. Cubrir regla de rating.
3. Cubrir errores de transicion invalida.
4. Probar casos de uso con fakes/mocks de puertos.
5. Asegurar cobertura alta en dominio.

### Comandos (PowerShell)

```powershell
cd backend
New-Item -ItemType File -Path tests\unit\test_idea_rules.py -Force
New-Item -ItemType File -Path tests\unit\test_rating_rules.py -Force
New-Item -ItemType File -Path tests\unit\test_update_idea_use_case.py -Force
uv run pytest tests/unit -q
```

### Criterios de aceptacion

- Reglas de dominio criticas cubiertas.
- Tests unitarios estables y rapidos.

---

## Ticket F6-03 - BDD con pytest-bdd

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F6-01`, `diseno-sistema-ideas-escenarios.md`

### Paso a paso

1. Instalar `pytest-bdd`.
2. Crear features iniciales `@mvp` desde escenarios.
3. Implementar step definitions.
4. Conectar steps con cliente API de pruebas.
5. Ejecutar subset de features criticas.

### Comandos (PowerShell)

```powershell
cd backend
uv add --dev pytest-bdd
New-Item -ItemType File -Path tests\bdd\features\auth.feature -Force
New-Item -ItemType File -Path tests\bdd\features\ideas.feature -Force
New-Item -ItemType File -Path tests\bdd\steps\test_auth_steps.py -Force
New-Item -ItemType File -Path tests\bdd\steps\test_ideas_steps.py -Force
uv run pytest tests/bdd -q
```

### Criterios de aceptacion

- Escenarios `@mvp` base ejecutables.
- Fallas expresan claramente regla incumplida.

---

## Ticket F6-04 - E2E con Playwright

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F5-*`

### Paso a paso

1. Instalar Playwright en frontend.
2. Configurar `playwright.config`.
3. Crear tests E2E de flujo principal:
   - login + crear idea
   - actualizar estado/progreso
   - agregar log
   - calificar idea
4. Configurar arranque de app para test.
5. Ejecutar E2E en local y CI.

### Comandos (PowerShell)

```powershell
cd frontend
npm install -D @playwright/test
npx playwright install
mkdir tests,e2e
New-Item -ItemType File -Path tests\e2e\ideas-flow.spec.ts -Force
npx playwright test
```

### Criterios de aceptacion

- `SCN-E2E-001..004` cubiertos.
- Suite E2E reproducible.

---

## Ticket F6-05 - Quality gates de cobertura y estabilidad

- Tipo: `TASK`
- Prioridad: `P1`
- Estimacion: `2 pts`
- Dependencias: `F6-01..F6-04`

### Paso a paso

1. Definir umbral de cobertura backend (ejemplo 80%).
2. Configurar fail en CI si baja cobertura.
3. Definir criterio minimo E2E (smoke obligatorio).
4. Publicar reporte de pruebas en pipeline.

### Comandos (PowerShell)

```powershell
cd backend
uv run pytest --cov=src --cov-fail-under=80
```

### Criterios de aceptacion

- Pipeline falla al romper umbral de calidad.

---

## 5. Mapeo rapido de escenarios a pruebas

- Auth API: `SCN-AUTH-*` -> integration + bdd.
- Ideas/progreso: `SCN-IDEA-*`, `SCN-PROG-*` -> unit + integration + bdd.
- Logs/rating: `SCN-LOG-*`, `SCN-RATE-*` -> integration + bdd.
- Flujo UI: `SCN-E2E-*` -> Playwright.

---

## 6. Checklist de cierre de Fase 6

- Pytest configurado con cobertura.
- Unit tests de dominio implementados.
- BDD de escenarios `@mvp` implementado.
- Playwright E2E operativo.
- Quality gates activos en CI local/pre-CI.

---

## 7. Definition of Done (DoD) Fase 6

La Fase 6 se considera cerrada cuando:
- Los escenarios criticos tienen pruebas automatizadas.
- Los tests son repetibles y estables.
- Existe gate de cobertura y gate de ejecucion E2E minima.
- El proyecto esta listo para industrializar entrega (Fase 8).
