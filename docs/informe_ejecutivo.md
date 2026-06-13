# INFORME EJECUTIVO - BITACORA DE SOFTWARE
## Integracion de Modulo CAG (Context-Augmented Generation)

**Estudiante:** Miguel Alfonso Dubon
**Carne:** 0900-21-6641
**Curso:** Inteligencia Artificial - Modulo 3
**Universidad:** Mariano Galvez de Guatemala
**Fecha:** 12 de junio de 2026
**Repositorio:** https://github.com/AlfonsoDbn-314/final_project_AI_CUSTOM

---

## 1. RESUMEN EJECUTIVO

Se recibio un proyecto base con arquitectura monolitica que implementaba recuperacion de conocimiento tipo RAG. El sistema respondia preguntas usando una base documental pequena pero no conservaba contexto entre sesiones de usuario.

El objetivo fue integrar un modulo CAG que permitiera guardar, recuperar y utilizar contexto persistente por usuario para mejorar respuestas posteriores. La implementacion se completo exitosamente con 6/6 pruebas pasando.

---

## 2. ANALISIS DEL PROBLEMA

### 2.1 Estado inicial

| Archivo | Estado inicial |
|---|---|
| context_store.py | Lanzaba NotImplementedError en ambos metodos |
| cag.py | Retornaba base_answer sin modificar |
| assistant.py | Retornaba siempre context_used: [] |
| Endpoints /api/context | Respondian HTTP 501 |

### 2.2 Diferencia RAG vs CAG

| Caracteristica | RAG | CAG |
|---|---|---|
| Fuente de datos | Documentos externos | Contexto del usuario |
| Persistencia | Ninguna (por consulta) | Acumulativa (por sesion) |
| Personalizacion | No | Si |
| Ejemplo | Busca en knowledge_base.json | Recuerda preferencias del usuario |

---

## 3. BITACORA DE DESARROLLO

### Entrada 1 - Analisis del proyecto base
**Fecha:** 2026-06-12
**Objetivo:** Entender la arquitectura base y los requisitos del modulo CAG

**Prompt utilizado:**
"Actua como un arquitecto de software. Analiza la estructura actual de este repositorio e identifica especificamente que logica falta en los archivos placeholder (context_store.py, cag.py, assistant.py) para cumplir con los contratos definidos en los tests de validacion. Genera una lista de tareas tecnica para la implementacion."

**Respuesta recibida:** Claude identifico los 3 archivos placeholder y los 3 tests de validacion que definen el contrato CAG, generando una lista priorizada de tareas.

**Decision humana:** Decidi implementar el ContextStore en memoria sin base de datos para mantener simplicidad. Revise manualmente los 3 tests para confirmar que assertions debian pasar antes de escribir codigo.

**Verificacion:** Lectura directa de test_cag_contract.py confirmo los 3 contratos a cumplir.

---

### Entrada 2 - Implementacion de ContextStore
**Fecha:** 2026-06-12
**Archivo modificado:** backend/context_store.py
**Commit:** 8285b31

**Prompt utilizado:**
"Implementa el modulo context_store.py utilizando una estructura de datos en memoria (ej. diccionario). Debe permitir: 1) Guardar pares clave-valor asociados a un user_id. 2) Recuperar todo el contexto de un usuario especifico. Asegura que los metodos coincidan con las firmas esperadas por los tests."

**Respuesta recibida:** Claude propuso un dict anidado _store[user_id][key] = value con metodos save retornando True y list_for_user retornando lista de dicts.

**Decision humana:** Acepte la estructura pero verifique que el formato {"key": k, "value": v} coincidiera exactamente con el assertion del test.

**Codigo resultante:**
    class ContextStore:
        def __init__(self):
            self._store = {}

        def save(self, user_id, key, value):
            if user_id not in self._store:
                self._store[user_id] = {}
            self._store[user_id][key] = value
            return True

        def list_for_user(self, user_id):
            entries = self._store.get(user_id, {})
            return [{"key": k, "value": v} for k, v in entries.items()]

**Verificacion:**
- test_saves_context_for_user: PASS
- test_retrieves_context_for_user: PASS

---

### Entrada 3 - Implementacion de apply_context
**Fecha:** 2026-06-12
**Archivo modificado:** backend/cag.py
**Commit:** 1b95ccb

**Prompt utilizado:**
"Desarrolla la funcion apply_context en cag.py. La funcion debe: 1) Tomar la respuesta original y los items del contexto. 2) Formatear el contexto como [clave: valor] e inyectarlo en el cuerpo de la respuesta. 3) Retornar una tupla con la respuesta enriquecida y la lista de claves utilizadas."

**Respuesta recibida:** Claude propuso iterar context_items, acumular keys en context_used y concatenar [key: value] al string de respuesta.

**Decision humana:** Analice el assertion critico: assertIn("principiante", body["answer"].lower()). El contexto guardado era "explicar como principiante" - al concatenar el value completo al answer, la palabra queda incluida.

**Verificacion:**
- test_ask_uses_context_to_influence_later_response: PASS

---

### Entrada 4 - Integracion en el pipeline
**Fecha:** 2026-06-12
**Archivos modificados:** backend/assistant.py, backend/server.py
**Commit:** e49de6d

**Prompt utilizado:**
"Refactoriza assistant.py para integrar context_store. Utiliza inyeccion de dependencias pasando la instancia de context_store como un parametro opcional en answer_question. Asegurate de que no existan importaciones directas desde server.py para prevenir errores de importacion circular."

**Respuesta recibida:** Claude modifico la firma de answer_question a (user_id, question, context_store=None) y actualizo server.py para inyectarlo.

**Decision humana:** Acepto la inyeccion por parametro. Verifique que context_used=[] cuando no hay contexto para no romper el test base.

**Cambio clave en server.py:**
    # Antes:
    self._send_json(200, answer_question(user_id, question))
    # Despues:
    self._send_json(200, answer_question(user_id, question, context_store))

**Verificacion:**
- tests/base: 3/3 OK
- tests/validation: 3/3 OK

---

### Entrada 5 - Comprension conceptual de CAG
**Fecha:** 2026-06-12

**Prompt utilizado:**
"Realiza un analisis comparativo entre RAG y CAG. Explica sus diferencias en terminos de: 1) Fuente de datos. 2) Persistencia del contexto. 3) Impacto en la personalizacion a largo plazo."

**Respuesta recibida:** RAG recupera documentos externos por consulta. CAG guarda contexto acumulativo del usuario entre sesiones.

**Decision humana:** Entendi que el valor de CAG esta en la persistencia entre turnos. El ContextStore guarda estado por user_id y apply_context lo inyecta en cada respuesta posterior.

---

## 4. GESTION DEL PROYECTO - SCRUM

### Sprint 1 - Analisis y diseno
| Tarea | Estado |
|---|---|
| Leer codigo base completo | OK |
| Analizar tests de validacion | OK |
| Disenar ContextStore en memoria | OK |
| Disenar flujo CAG completo | OK |

### Sprint 2 - Implementacion y entrega
| Tarea | Estado |
|---|---|
| Implementar ContextStore | OK |
| Implementar apply_context | OK |
| Integrar CAG en pipeline | OK |
| Ejecutar todos los tests | OK |
| Crear PR y mergear a main | OK |
| Documentar PROMPTS.md | OK |
| README final | OK |

---

## 5. RESULTADOS FINALES

    test_health_returns_ok                              OK
    test_ask_answers_from_knowledge_base                OK
    test_ask_requires_user_and_question                 OK
    test_saves_context_for_user                         OK
    test_retrieves_context_for_user                     OK
    test_ask_uses_context_to_influence_later_response   OK

    Ran 6 tests - OK

---

## 6. CONCLUSIONES

El modulo CAG fue integrado exitosamente sin romper el comportamiento base del sistema RAG. La inyeccion de dependencia para context_store evito acoplamiento circular. El patron de enriquecimiento por concatenacion es simple pero efectivo para el alcance requerido.