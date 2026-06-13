# PROMPTS.md — Registro de uso de IA

## Entrada 1
**Fecha:** 2026-06-12
**Objetivo:** Entender la arquitectura base del proyecto y los requisitos del módulo CAG
**Prompt usado:** "Revisa este repo y analiza qué hay que implementar para pasar los tests de validación"
**Resumen de respuesta:** Claude identificó los 3 archivos placeholder (context_store.py, cag.py, assistant.py) y los 3 tests de validación que definen el contrato CAG
**Decisión humana:** Decidí implementar el ContextStore en memoria (sin base de datos) para mantener simplicidad en el alcance del examen
**Cambios realizados:** Lectura del código base, identificación de los puntos de integración
**Verificación:** Revisé manualmente los 3 tests para confirmar qué assertions debían pasar

## Entrada 2
**Fecha:** 2026-06-12
**Objetivo:** Implementar ContextStore funcional
**Prompt usado:** "Necesito implementar context_store.py para que guarde y recupere contexto por user_id en memoria"
**Resumen de respuesta:** Claude propuso un dict anidado _store[user_id][key] = value con métodos save y list_for_user
**Decisión humana:** Acepté la estructura de dict en memoria, verifiqué que el formato de retorno {key, value} coincidiera con lo que exige el test
**Cambios realizados:** backend/context_store.py implementado
**Verificación:** Ejecuté test_saves_context_for_user y test_retrieves_context_for_user manualmente

## Entrada 3
**Fecha:** 2026-06-12
**Objetivo:** Implementar apply_context en cag.py
**Prompt usado:** "Implementa apply_context para que enriquezca la respuesta con el contexto del usuario e indique qué claves usó"
**Resumen de respuesta:** Claude propuso iterar context_items, concatenar [key: value] a la respuesta y retornar lista de claves usadas
**Decisión humana:** Verifiqué que la palabra del contexto (ej: "principiante") quedara incluida en el answer para satisfacer el assertion del test
**Cambios realizados:** backend/cag.py implementado
**Verificación:** Ejecuté test_ask_uses_context_to_influence_later_response y confirmé que pasaba

## Entrada 4
**Fecha:** 2026-06-12
**Objetivo:** Integrar CAG en el pipeline de answer_question
**Prompt usado:** "Integra context_store en assistant.py evitando importación circular con server.py"
**Resumen de respuesta:** Claude propuso pasar context_store como parámetro opcional a answer_question y actualizar server.py para inyectarlo
**Decisión humana:** Acepté la inyección por parámetro como patrón más limpio y mantenible
**Cambios realizados:** backend/assistant.py y backend/server.py modificados
**Verificación:** Ejecuté los 6 tests (3 base + 3 validación) y todos pasaron OK

## Entrada 5
**Fecha:** 2026-06-12
**Objetivo:** Comprender conceptualmente CAG y su diferencia con RAG
**Prompt usado:** "Explica la diferencia entre RAG y CAG y por que CAG mejora respuestas futuras"
**Resumen de respuesta:** RAG recupera documentos externos en cada consulta (estatico por pregunta). CAG guarda contexto acumulativo del usuario entre sesiones: preferencias, historial, decisiones. RAG responde con conocimiento externo, CAG personaliza con conocimiento del usuario.
**Decision humana:** Entendi que el valor de CAG esta en la persistencia entre turnos, no en recuperar documentos. Por eso el ContextStore guarda estado por user_id y apply_context lo inyecta en cada respuesta posterior.
**Cambios realizados:** Esta comprension guio el diseno completo del modulo.
**Verificacion:** El test test_ask_uses_context_to_influence_later_response valida exactamente este comportamiento: guardar contexto en un turno y usarlo en el siguiente.