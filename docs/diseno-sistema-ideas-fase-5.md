# Fase 5 - Frontend en Next.js por Modulos/Features (Tickets + Pasos + Comandos)

## 1. Objetivo de la fase

Implementar una UI funcional y modular en Next.js que consuma la API v1 del backend para cubrir el flujo completo del usuario: login, CRUD de ideas, progreso/estado, logs y rating.

## 1.1 Fuentes base

- `diseno-sistema-ideas.md`
- `diseno-sistema-ideas-backlog.md`
- `diseno-sistema-ideas-escenarios.md`
- `diseno-sistema-ideas-fase-4.md`

---

## 2. Orden de ejecucion recomendado (Fase 5)

1. `F5-01` Feature `auth` (login y sesion).
2. `F5-02` Feature `ideas` (listado y crear).
3. `F5-03` Feature `ideas` (detalle y actualizar).
4. `F5-04` Feature `progress-logs` (textarea + timeline).
5. `F5-05` Feature `ratings`.
6. `F5-07` Guard de rutas privadas.
7. `F5-06` Manejo global de errores y loading.

---

## 3. Estructura objetivo frontend

```text
frontend/
  src/
    app/
      (public)/login/page.tsx
      (private)/ideas/page.tsx
      (private)/ideas/[ideaId]/page.tsx
    modules/
      auth/
      ideas/
      progress-logs/
      ratings/
    shared/
      lib/
      ui/
      config/
```

---

## 4. Tickets de Fase 5 (detalle paso a paso)

## Ticket F5-01 - Feature auth: pantalla login y sesion

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F3-01`, `F4-01`

### Paso a paso

1. Crear modulo `auth` con `components`, `services`, `hooks`.
2. Implementar formulario login.
3. Consumir `POST /api/v1/auth/login`.
4. Guardar token en almacenamiento seguro de cliente.
5. Redirigir a `/ideas` en login exitoso.
6. Manejar error `401` en UI.

### Comandos (PowerShell)

```powershell
cd frontend
mkdir src\modules\auth\components,src\modules\auth\services,src\modules\auth\hooks,src\modules\auth\model
New-Item -ItemType File -Path src\modules\auth\components\LoginForm.tsx -Force
New-Item -ItemType File -Path src\modules\auth\services\authApi.ts -Force
New-Item -ItemType File -Path src\modules\auth\hooks\useLogin.ts -Force
```

### Criterios de aceptacion

- Login exitoso guarda token y navega a `/ideas`.
- Login invalido muestra error de credenciales.

---

## Ticket F5-02 - Feature ideas: listado y crear idea

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F4-01`, `F4-02`

### Paso a paso

1. Crear pagina `/ideas`.
2. Implementar fetch de `GET /ideas`.
3. Crear formulario de alta (titulo/descripcion).
4. Consumir `POST /ideas`.
5. Refrescar listado tras crear.
6. Mostrar estados de loading/empty.

### Comandos (PowerShell)

```powershell
cd frontend
mkdir src\modules\ideas\components,src\modules\ideas\services,src\modules\ideas\hooks,src\modules\ideas\model
New-Item -ItemType File -Path src\modules\ideas\components\IdeaForm.tsx -Force
New-Item -ItemType File -Path src\modules\ideas\components\IdeaCard.tsx -Force
New-Item -ItemType File -Path src\modules\ideas\services\ideasApi.ts -Force
```

### Criterios de aceptacion

- Lista visible con ideas activas.
- Alta de idea funcional desde UI.

---

## Ticket F5-03 - Feature ideas: detalle y actualizacion

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `5 pts`
- Dependencias: `F4-03`, `F4-04`

### Paso a paso

1. Crear pagina `/ideas/[ideaId]`.
2. Cargar detalle por id.
3. Implementar controles de estado y progreso.
4. Consumir `PATCH /ideas/{id}`.
5. Mostrar validaciones de negocio (400/422).

### Comandos (PowerShell)

```powershell
cd frontend
New-Item -ItemType File -Path src\modules\ideas\components\IdeaStatusBadge.tsx -Force
New-Item -ItemType File -Path src\modules\ideas\components\ExecutionProgressBar.tsx -Force
New-Item -ItemType File -Path src\modules\ideas\hooks\useIdeaDetail.ts -Force
New-Item -ItemType File -Path src\modules\ideas\hooks\useIdeaMutations.ts -Force
```

### Criterios de aceptacion

- Detalle muestra estado/progreso actual.
- Actualizacion valida persiste y refresca UI.

---

## Ticket F5-04 - Feature progress-logs: textarea + timeline

- Tipo: `STORY`
- Prioridad: `P0`
- Estimacion: `3 pts`
- Dependencias: `F4-06`, `F4-07`

### Paso a paso

1. Crear modulo `progress-logs`.
2. Implementar textarea para agregar comentario.
3. Consumir `POST /ideas/{id}/logs`.
4. Implementar timeline y consumir `GET /ideas/{id}/logs`.
5. Ordenar y renderizar por fecha.

### Comandos (PowerShell)

```powershell
cd frontend
mkdir src\modules\progress-logs\components,src\modules\progress-logs\services,src\modules\progress-logs\hooks
New-Item -ItemType File -Path src\modules\progress-logs\components\ProgressLogTextarea.tsx -Force
New-Item -ItemType File -Path src\modules\progress-logs\components\ProgressLogTimeline.tsx -Force
New-Item -ItemType File -Path src\modules\progress-logs\services\progressLogsApi.ts -Force
```

### Criterios de aceptacion

- Comentario se registra y aparece en timeline.
- Timeline refresca tras alta.

---

## Ticket F5-05 - Feature ratings: registrar calificacion final

- Tipo: `STORY`
- Prioridad: `P1`
- Estimacion: `3 pts`
- Dependencias: `F4-08`

### Paso a paso

1. Crear modulo `ratings`.
2. Implementar formulario de rating (1..10).
3. Consumir `POST/PATCH /ideas/{id}/rating`.
4. Consumir `GET /ideas/{id}/rating`.
5. Mostrar errores si idea no esta terminada.

### Comandos (PowerShell)

```powershell
cd frontend
mkdir src\modules\ratings\components,src\modules\ratings\services,src\modules\ratings\hooks
New-Item -ItemType File -Path src\modules\ratings\components\IdeaRatingForm.tsx -Force
New-Item -ItemType File -Path src\modules\ratings\components\IdeaRatingSummary.tsx -Force
New-Item -ItemType File -Path src\modules\ratings\services\ratingsApi.ts -Force
```

### Criterios de aceptacion

- Permite registrar/editar rating en ideas terminadas.
- Rechaza en UI cuando no aplica.

---

## Ticket F5-07 - Guard de rutas privadas

- Tipo: `TASK`
- Prioridad: `P1`
- Estimacion: `2 pts`
- Dependencias: `F5-01`

### Paso a paso

1. Definir middleware o guard por layout privado.
2. Verificar token antes de navegar a rutas privadas.
3. Redirigir a login cuando sesion invalida.
4. Manejar expiracion de token.

### Comandos (PowerShell)

```powershell
cd frontend
New-Item -ItemType File -Path src\middleware.ts -Force
```

### Criterios de aceptacion

- Rutas privadas inaccesibles sin autenticacion.

---

## Ticket F5-06 - Manejo global de errores y loading

- Tipo: `TASK`
- Prioridad: `P1`
- Estimacion: `2 pts`
- Dependencias: `F5-01..F5-05`

### Paso a paso

1. Crear `apiClient` central con interceptores.
2. Estandarizar parseo de errores (`code`, `message`, `details`).
3. Agregar estados loading/skeleton por pantalla.
4. Definir fallback de error global.

### Comandos (PowerShell)

```powershell
cd frontend
mkdir src\shared\lib
New-Item -ItemType File -Path src\shared\lib\apiClient.ts -Force
New-Item -ItemType File -Path src\app\error.tsx -Force
New-Item -ItemType File -Path src\app\loading.tsx -Force
```

### Criterios de aceptacion

- UX consistente en carga y errores.

---

## 5. Trazabilidad Fase 5 (ticket -> escenarios)

| Ticket | Escenarios impactados | Validacion principal |
|---|---|---|
| F5-01 | SCN-E2E-001 | E2E |
| F5-02 | SCN-E2E-001 | E2E |
| F5-03 | SCN-E2E-002 | E2E |
| F5-04 | SCN-E2E-003 | E2E |
| F5-05 | SCN-E2E-004 | E2E |
| F5-07 | SCN-AUTH-003, SCN-AUTH-004 | Integracion UI |
| F5-06 | Todos los E2E de fase | UX/Integracion |

---

## 6. Checklist de cierre de Fase 5

- Login y sesion operativos.
- Listado/alta/detalle/actualizacion de ideas operativos.
- Logs de progreso operativos.
- Rating operativo.
- Guard de rutas privadas activo.
- Errores/loading estandarizados.

---

## 7. Definition of Done (DoD) Fase 5

La Fase 5 se considera cerrada cuando:
- El flujo `SCN-E2E-001..004` es ejecutable desde UI.
- Frontend esta organizado por modulos/features.
- El consumo de API esta centralizado y tipado.
- Queda base lista para automatizacion completa en Fase 6.
