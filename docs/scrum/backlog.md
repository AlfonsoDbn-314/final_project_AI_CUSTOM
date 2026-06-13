# Product Backlog

## US-01 — Guardar contexto de usuario
Como sistema CAG, necesito persistir pares clave-valor por usuario para enriquecer respuestas futuras.
**Criterio de aceptación:** POST /api/context retorna 201 con saved=true

## US-02 — Recuperar contexto de usuario
Como sistema CAG, necesito recuperar el contexto almacenado de un usuario dado.
**Criterio de aceptación:** GET /api/context?user_id=X retorna lista de {key, value}

## US-03 — Usar contexto en respuestas
Como asistente, necesito incorporar el contexto del usuario en mis respuestas para personalizarlas.
**Criterio de aceptación:** La respuesta incluye términos del contexto y context_used lista las claves utilizadas

## US-04 — Mantener tests base sin regresiones
Como desarrollador, necesito que los 3 tests base sigan pasando tras integrar CAG.
**Criterio de aceptación:** 3/3 tests base OK
