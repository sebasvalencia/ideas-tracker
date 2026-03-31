# Kanban de Ejecucion - Ideas Tracker (1 Developer)

## 1) Objetivo

Usar este documento como tablero operativo semanal para mover tickets entre columnas:

- `To Do`
- `Doing`
- `Review`
- `Done`

Regla principal:

- Mantener `WIP=1` en `Doing`.

---

## 2) Politica de movimiento entre columnas

- `To Do -> Doing`
  - Dependencias cumplidas.
  - Ticket entendido y acotado.
- `Doing -> Review`
  - Implementacion terminada.
  - Pruebas locales del ticket en verde.
- `Review -> Done`
  - Criterios de aceptacion cumplidos.
  - Escenarios `SCN-*` relacionados validados.
  - Documentacion actualizada.

---

## 3) Semana 1 (Fase 0 + Fase 1)

### To Do

- F0-01
- F0-02
- F0-03
- F0-04
- F1-01
- F1-02
- F1-03
- F1-04
- F1-05
- F1-06

### Doing

- F0-01

### Review

- (vacio)

### Done

- (vacio)

Meta de semana:

- Cerrar Fase 0 y Fase 1 completas.

---

## 4) Semana 2 (Fase 2 + inicio Fase 3)

### To Do

- F2-01
- F2-02
- F2-03
- F2-04
- F2-05
- F2-06
- F3-01
- F3-02

### Doing

- F2-01

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado de Semana 1

Meta de semana:

- Persistencia completa y auth base iniciada.

---

## 5) Semana 3 (cierre Fase 3 + inicio Fase 4)

### To Do

- F3-03
- F3-05
- F3-04 (opcional)
- F4-01
- F4-02
- F4-03
- F4-04

### Doing

- F3-03

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 2

Meta de semana:

- Seguridad base completa + CRUD principal iniciado.

---

## 6) Semana 4 (cierre Fase 4 + inicio Fase 5)

### To Do

- F4-06
- F4-07
- F4-09
- F4-08
- F4-05
- F5-01
- F5-02
- F5-03

### Doing

- F4-06

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 3

Meta de semana:

- API dominio completa + frontend base funcional.

---

## 7) Semana 5 (cierre Fase 5 + inicio Fase 6)

### To Do

- F5-04
- F5-05
- F5-07
- F5-06
- F6-01
- F6-02
- F6-03

### Doing

- F5-04

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 4

Meta de semana:

- Flujo UI completo + pruebas de base.

---

## 8) Semana 6 (cierre Fase 6 + Fase 8)

### To Do

- F6-04
- F6-05
- F8-01
- F8-02
- F8-03
- F8-04
- F8-05

### Doing

- F6-04

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 5

Meta de semana:

- Calidad automatizada + CI/CD y contenedores listos.

---

## 9) Semana 7 (Fase 7 + inicio Fase 9)

### To Do

- F7-01
- F7-02
- F7-03
- F7-04
- F7-05
- F9-01
- F9-02

### Doing

- F7-01

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 6

Meta de semana:

- Observabilidad activa y base K8s desplegada.

---

## 10) Semana 8 (cierre Fase 9 + estabilizacion)

### To Do

- F9-03
- F9-04
- F9-05
- Estabilizacion final

### Doing

- F9-03

### Review

- (vacio)

### Done

- Arrastrar todo lo cerrado hasta Semana 7

Meta de semana:

- Hardening productivo y baseline de rendimiento.

---

## 11) Mapa rapido de escenarios por semana

- Semana 3-4:
  - `SCN-AUTH-*`
  - `SCN-IDEA-*`
  - `SCN-PROG-*`
- Semana 4-5:
  - `SCN-LOG-*`
  - `SCN-RATE-*`
- Semana 5-6:
  - `SCN-E2E-001..004`
- Semana 7-8:
  - `SCN-OBS-*`
  - `SCN-SEC-*` (hardening adicional)

---

## 12) Cierre semanal (checklist operativo)

- Todos los tickets en `Done` cumplen criterios de aceptacion.
- No quedan tickets bloqueados sin accion definida.
- `Doing` queda con 1 ticket maximo.
- Se actualizaron evidencias de pruebas y escenarios.
- Se registraron riesgos y ajustes para la semana siguiente.

