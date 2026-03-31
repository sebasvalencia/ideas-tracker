# Solucion F1-04 (Hexagonal Stub) - Puertos, Use Case, Endpoint y Verificacion

Este documento resuelve de forma concreta los puntos de `F1-04`:

1. Definir puertos iniciales de repositorio/seguridad.
2. Implementar un caso de uso de ejemplo (`CreateIdea` stub).
3. Exponer endpoint REST conectado al caso de uso (stub).
4. Verificar separacion de dependencias hacia adentro.

Se toma como base:
- `docs/diseno-sistema-ideas-fase-1.md`
- `diseno-sistema-ideas-backlog.md`
- `diseno-sistema-ideas-escenarios.md`
- Estado actual de `backend/src/main.py`.

---

## 1) Estructura minima recomendada

```text
backend/
  src/
    main.py
    app/
      domain/
        idea/
          entities.py
      application/
        idea/
          dto.py
          ports.py
          use_cases/
            create_idea.py
      adapters/
        inbound/
          rest/
            routers/
              ideas_router.py
        outbound/
          persistence/
            in_memory/
              idea_repository.py
          security/
            auth_context.py
      bootstrap/
        container.py
```

Nota: para este ticket usamos repositorio `in_memory` (stub) para validar arquitectura antes de SQLAlchemy (Fase 2).

---

## 2) Puertos iniciales (repositorio/seguridad)

Archivo sugerido: `backend/src/app/application/idea/ports.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AuthUser:
    user_id: int
    email: str
    role: str


class IdeaRepositoryPort(Protocol):
    def create(self, *, owner_id: int, title: str, description: str) -> "IdeaRecord":
        ...


class AuthContextPort(Protocol):
    def current_user(self) -> AuthUser:
        ...


@dataclass(frozen=True)
class IdeaRecord:
    id: int
    owner_id: int
    title: str
    description: str
    status: str
    execution_percentage: float
```

Decisiones:
- `IdeaRepositoryPort` representa salida a persistencia.
- `AuthContextPort` abstrae usuario autenticado (salida de seguridad para capa application).

---

## 3) Caso de uso `CreateIdea` (stub)

### DTOs

Archivo: `backend/src/app/application/idea/dto.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateIdeaInput:
    title: str
    description: str


@dataclass(frozen=True)
class CreateIdeaOutput:
    id: int
    owner_id: int
    title: str
    description: str
    status: str
    execution_percentage: float
```

### Use Case

Archivo: `backend/src/app/application/idea/use_cases/create_idea.py`

```python
from app.application.idea.dto import CreateIdeaInput, CreateIdeaOutput
from app.application.idea.ports import AuthContextPort, IdeaRepositoryPort


class CreateIdeaUseCase:
    def __init__(self, repo: IdeaRepositoryPort, auth_ctx: AuthContextPort) -> None:
        self._repo = repo
        self._auth_ctx = auth_ctx

    def execute(self, data: CreateIdeaInput) -> CreateIdeaOutput:
        if not data.title.strip():
            raise ValueError("title must not be empty")
        if not data.description.strip():
            raise ValueError("description must not be empty")

        user = self._auth_ctx.current_user()
        created = self._repo.create(
            owner_id=user.user_id,
            title=data.title.strip(),
            description=data.description.strip(),
        )
        return CreateIdeaOutput(
            id=created.id,
            owner_id=created.owner_id,
            title=created.title,
            description=created.description,
            status=created.status,
            execution_percentage=created.execution_percentage,
        )
```

---

## 4) Endpoint REST conectado al Use Case (stub)

### Router

Archivo: `backend/src/app/adapters/inbound/rest/routers/ideas_router.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.idea.dto import CreateIdeaInput
from app.bootstrap.container import get_create_idea_use_case

router = APIRouter(prefix="/api/v1/ideas", tags=["ideas"])


class CreateIdeaRequest(BaseModel):
    title: str
    description: str


@router.post("", status_code=201)
def create_idea(payload: CreateIdeaRequest):
    use_case = get_create_idea_use_case()
    try:
        result = use_case.execute(
            CreateIdeaInput(
                title=payload.title,
                description=payload.description,
            )
        )
        return result.__dict__
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
```

### Container/Wiring (stub)

Archivo: `backend/src/app/bootstrap/container.py`

```python
from app.adapters.outbound.persistence.in_memory.idea_repository import InMemoryIdeaRepository
from app.adapters.outbound.security.auth_context import StaticAuthContext
from app.application.idea.use_cases.create_idea import CreateIdeaUseCase

_repo = InMemoryIdeaRepository()
_auth = StaticAuthContext()


def get_create_idea_use_case() -> CreateIdeaUseCase:
    return CreateIdeaUseCase(repo=_repo, auth_ctx=_auth)
```

### Adaptadores stub outbound

Archivo: `backend/src/app/adapters/outbound/persistence/in_memory/idea_repository.py`

```python
from app.application.idea.ports import IdeaRecord


class InMemoryIdeaRepository:
    def __init__(self) -> None:
        self._seq = 0
        self._items: list[IdeaRecord] = []

    def create(self, *, owner_id: int, title: str, description: str) -> IdeaRecord:
        self._seq += 1
        item = IdeaRecord(
            id=self._seq,
            owner_id=owner_id,
            title=title,
            description=description,
            status="idea",
            execution_percentage=0.0,
        )
        self._items.append(item)
        return item
```

Archivo: `backend/src/app/adapters/outbound/security/auth_context.py`

```python
from app.application.idea.ports import AuthUser


class StaticAuthContext:
    def current_user(self) -> AuthUser:
        # Stub temporal para F1-04; se reemplaza por JWT en Fase 3.
        return AuthUser(user_id=1, email="dev@local", role="user")
```

### Integracion en `main.py`

Archivo actual: `backend/src/main.py`

```python
from fastapi import FastAPI
from app.adapters.inbound.rest.routers.ideas_router import router as ideas_router

app = FastAPI(title="Ideas Tracker API")
app.include_router(ideas_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

---

## 5) Verificacion de dependencias hacia adentro

Regla hexagonal:
- `domain` no importa `fastapi`, `sqlalchemy`, `pydantic`.
- `application` no importa `fastapi` ni `sqlalchemy`.
- `adapters/inbound` solo llama use cases.
- `adapters/outbound` implementa puertos de `application`.

Checklist de verificacion:
- [ ] Use case solo conoce puertos (`IdeaRepositoryPort`, `AuthContextPort`).
- [ ] Router no contiene logica de negocio.
- [ ] Repositorio in-memory no depende de FastAPI.
- [ ] `main.py` solo realiza wiring de entrada.

Comandos utiles:

```powershell
cd backend
uv run uvicorn src.main:app --reload --port 8000

# Probar endpoint stub
curl -X POST http://localhost:8000/api/v1/ideas `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"Idea demo\",\"description\":\"Prueba stub\"}"
```

Resultado esperado:
- `201 Created` con idea en estado `idea` y `execution_percentage = 0.0`.

---

## 6) Criterio de aceptacion de este entregable

Se considera resuelto F1-04 (stub) cuando:
- Existen puertos iniciales de repositorio y seguridad.
- `CreateIdeaUseCase` funciona con adaptadores stub.
- Endpoint REST `/api/v1/ideas` esta conectado al use case.
- Se demuestra separacion de capas sin acoplamiento indebido.

---

## 7) Siguiente evolucion (Fase 2/Fase 3)

- Fase 2: reemplazar repo in-memory por SQLAlchemy repository.
- Fase 3: reemplazar `StaticAuthContext` por contexto real JWT.
