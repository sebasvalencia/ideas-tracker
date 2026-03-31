# Guia de Ejecucion de Fases - Ideas Tracker

## 1) Objetivo

Tener una ruta unica, clara y ejecutable para desarrollar el proyecto completo como **1 developer**, siguiendo los documentos de fases ya creados.

Documentos base:
- `diseno-sistema-ideas.md`
- `diseno-sistema-ideas-backlog.md`
- `diseno-sistema-ideas-escenarios.md`
- `diseno-sistema-ideas-fase-0.md` ... `diseno-sistema-ideas-fase-9.md`

---

## 2) Orden oficial de ejecucion

1. Fase 0 - Descubrimiento y alineacion.
2. Fase 1 - Base arquitectura y repositorio.
3. Fase 2 - Modelo de datos y persistencia.
4. Fase 3 - Seguridad y autenticacion.
5. Fase 4 - API de dominio.
6. Fase 5 - Frontend por modulos/features.
7. Fase 6 - Calidad, BDD y pruebas.
8. Fase 8 - Contenerizacion y CI/CD inicial.
9. Fase 7 - Observabilidad.
10. Fase 9 - Kubernetes y hardening productivo.

Nota: Fase 8 se ejecuta antes que Fase 7 para acelerar entrega continua y validacion temprana en pipeline.

---

## 3) Plan sugerido por semanas (1 developer)

### Semana 1
- Fase 0 completa.
- Fase 1 completa.

### Semana 2
- Fase 2 completa.
- Inicio Fase 3 (`F3-01`, `F3-02`).

### Semana 3
- Cierre Fase 3.
- Inicio Fase 4 (`F4-01` a `F4-04`).

### Semana 4
- Cierre Fase 4 (`F4-05` a `F4-09`).
- Inicio Fase 5 (`F5-01`, `F5-02`, `F5-03`).

### Semana 5
- Cierre Fase 5.
- Inicio Fase 6 (`F6-01`, `F6-02`, `F6-03`).

### Semana 6
- Cierre Fase 6 (`F6-04`, `F6-05`).
- Fase 8 completa.

### Semana 7
- Fase 7 completa.
- Inicio Fase 9 (`F9-01`, `F9-02`).

### Semana 8
- Cierre Fase 9 (`F9-03`, `F9-04`, `F9-05`).
- Estabilizacion final.

---

## 4) Regla operativa diaria (para avanzar sin bloqueo)

1. Elegir **1 ticket** activo (`WIP=1`).
2. Implementar codigo.
3. Ejecutar pruebas del ticket.
4. Validar escenarios relacionados (`SCN-*`).
5. Actualizar documentacion minima.
6. Cerrar ticket solo si cumple DoD.

---

## 5) Checklist por ticket (plantilla rapida)

- [ ] Ticket con objetivo y alcance claro.
- [ ] Dependencias satisfechas.
- [ ] Implementacion completada.
- [ ] Pruebas unitarias/integracion/E2E segun aplique.
- [ ] Escenarios mapeados (`SCN-*`) validados.
- [ ] Criterios de aceptacion cumplidos.
- [ ] Documentacion actualizada.

---

## 6) Hitos de control (quality gates)

### Gate A - Fin de Semana 2
- Backend base + DB + migraciones + auth inicial funcionando.

### Gate B - Fin de Semana 4
- API de dominio completa.
- Reglas de negocio validadas.

### Gate C - Fin de Semana 6
- Frontend funcional end-to-end.
- Pruebas BDD/E2E minimas en verde.
- CI/CD base operativa.

### Gate D - Fin de Semana 8
- Observabilidad basica activa.
- Despliegue Kubernetes con hardening inicial.

---

## 7) Riesgos frecuentes y accion inmediata

- Riesgo: abrir muchos tickets en paralelo.
  - Accion: volver a `WIP=1`.
- Riesgo: avanzar sin pruebas.
  - Accion: no cerrar ticket hasta tener cobertura minima.
- Riesgo: sobre-diseno temprano.
  - Accion: mantener foco en escenarios `@mvp`.
- Riesgo: retraso por infraestructura avanzada.
  - Accion: priorizar Fases 0-6 y 8 antes de 7/9.

---

## 8) Definicion de termino del proyecto (MVP + operacion)

Se considera completado cuando:
- Flujo completo `SCN-E2E-001..004` funciona estable.
- Escenarios `@mvp` estan automatizados y en verde.
- Pipeline CI corre en cada PR con gates de calidad.
- Sistema deployable por contenedor y operable en cluster.

---

## 9) Siguiente accion inmediata recomendada

Tomar `F0-01` en curso ahora mismo y completar Fase 0 antes de iniciar implementacion tecnica.
