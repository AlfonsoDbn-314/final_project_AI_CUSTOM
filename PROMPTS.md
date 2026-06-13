# PROMPTS.md — Registro de uso de IA

## Entrada 1
**Fecha:** 2026-06-12
**Objetivo:** Entender la arquitectura base del proyecto y los requisitos del módulo CAG
**Prompt usado:** "Actúa como un arquitecto de software. Analiza la estructura actual de este repositorio e identifica específicamente qué lógica falta en los archivos placeholder (context_store.py, cag.py, assistant.py) para cumplir con los contratos definidos en los tests de validación. Genera una lista de tareas técnica para la implementación."
**Resumen de respuesta:** Claude identificó los 3 archivos placeholder (context_store.py, cag.py, assistant.py) y los 3 tests de validación que definen el contrato CAG
**Decisión humana:** Decidí implementar el ContextStore en memoria (sin base de datos) para mantener simplicidad en el alcance del examen
**Cambios realizados:** Lectura del código base, identificación de los puntos de integración
**Verificación:** Revisé manualmente los 3 tests para confirmar qué assertions debían pasar

## Entrada 2
**Fecha:** 2026-06-12
**Objetivo:** Implementar ContextStore funcional
**Prompt usado:** "Implementa el módulo context_store.py utilizando una estructura de datos en memoria (ej. diccionario). Debe permitir: 1) Guardar pares clave-valor asociados a un user_id. 2) Recuperar todo el contexto de un usuario específico. Asegura que los métodos coincidan con las firmas esperadas por los tests."
**Resumen de respuesta:** Claude propuso un dict anidado _store[user_id][key] = value con métodos save y list_for_user
**Decisión humana:** Acepté la estructura de dict en memoria, verifiqué que el formato de retorno {key, value} coincidiera con lo que exige el test
**Cambios realizados:** backend/context_store.py implementado
**Verificación:** Ejecuté test_saves_context_for_user y test_retrieves_context_for_user manualmente

## Entrada 3
**Fecha:** 2026-06-12
**Objetivo:** Implementar apply_context en cag.py
**Prompt usado:** "Desarrolla la función apply_context en cag.py. La función debe: 1) Tomar la respuesta original y los ítems del contexto. 2) Formatear el contexto como [clave: valor] e inyectarlo en el cuerpo de la respuesta. 3) Retornar una tupla con la respuesta enriquecida y la lista de claves utilizadas."
**Resumen de respuesta:** Claude propuso iterar context_items, concatenar [key: value] a la respuesta y retornar lista de claves usadas
**Decisión humana:** Verifiqué que la palabra del contexto (ej: "principiante") quedara incluida en el answer para satisfacer el assertion del test
**Cambios realizados:** backend/cag.py implementado
**Verificación:** Ejecuté test_ask_uses_context_to_influence_later_response y confirmé que pasaba

## Entrada 4
**Fecha:** 2026-06-12
**Objetivo:** Integrar CAG en el pipeline de answer_question
**Prompt usado:** "Refactoriza assistant.py para integrar context_store. Utiliza inyección de dependencias pasando la instancia de context_store como un parámetro opcional en answer_question. Asegúrate de que no existan importaciones directas desde server.py para prevenir errores de importación circular."
**Resumen de respuesta:** Claude propuso pasar context_store como parámetro opcional a answer_question y actualizar server.py para inyectarlo
**Decisión humana:** Acepté la inyección por parámetro como patrón más limpio y mantenible
**Cambios realizados:** backend/assistant.py y backend/server.py modificados
**Verificación:** Ejecuté los 6 tests (3 base + 3 validación) y todos pasaron OK

## Entrada 5
**Fecha:** 2026-06-12
**Objetivo:** Comprender conceptualmente CAG y su diferencia con RAG
**Prompt usado:** "Realiza un análisis comparativo entre RAG (Retrieval-Augmented Generation) y CAG (Context-Augmented Generation). Explica sus diferencias en términos de: 1) Fuente de datos. 2) Persistencia del contexto del usuario. 3) Impacto en la personalización a largo plazo. Detalla por qué CAG es superior para mantener la coherencia en sesiones múltiples."
**Resumen de respuesta:** RAG recupera documentos externos en cada consulta (estatico por pregunta). CAG guarda contexto acumulativo del usuario entre sesiones: preferencias, historial, decisiones. RAG responde con conocimiento externo, CAG personaliza con conocimiento del usuario.
**Decision humana:** Entendi que el valor de CAG esta en la persistencia entre turnos, no en recuperar documentos. Por eso el ContextStore guarda estado por user_id y apply_context lo inyecta en cada respuesta posterior.
**Cambios realizados:** Esta comprension guio el diseno completo del modulo.
**Verificacion:** El test test_ask_uses_context_to_influence_later_response valida exactamente este comportamiento: guardar contexto en un turno y usarlo en el siguiente.