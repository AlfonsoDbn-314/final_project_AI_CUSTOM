# Proyecto Examen Final - Modulo 3

**Estudiante:** Miguel Alfonso Dubon - 0900-21-6641
**Curso:** Inteligencia Artificial - Universidad Mariano Galvez de Guatemala

## Descripcion

Proyecto monolitico con frontend, backend RAG y modulo CAG integrado. El sistema responde preguntas usando una base documental y enriquece las respuestas con contexto persistente por usuario.

## Modulo CAG implementado

- `backend/context_store.py` - almacenamiento en memoria de contexto por usuario
- `backend/cag.py` - logica de enriquecimiento de respuestas con contexto
- `backend/assistant.py` - pipeline integrado RAG + CAG

## Ejecutar backend

    PYTHONPATH=. python3 -m backend.server

El backend queda disponible en http://127.0.0.1:8000

## Ejecutar pruebas base

    PYTHONPATH=. python -m unittest discover -s tests/base -p "test_*.py" -v

## Ejecutar pruebas de validacion

    PYTHONPATH=. python -m unittest discover -s tests/validation -p "test_*.py" -v

## Resultados de pruebas

- tests/base: 3/3 OK
- tests/validation: 3/3 OK

## Estructura

| Ruta | Contenido |
|---|---|
| backend/ | Servidor, RAG y modulo CAG |
| frontend/ | Interfaz web estatica |
| data/ | Base de conocimiento |
| tests/base/ | Pruebas base del proyecto |
| tests/validation/ | Pruebas de validacion CAG |
| docs/scrum/ | Backlog, Sprint 1 y Sprint 2 |
| docs/evidencias/ | Capturas del proceso |
| PROMPTS.md | Registro cronologico de uso de IA |

## Proceso

- Metodologia: Scrum con 2 sprints
- Control de versiones: branch develop, PR mergeado a main
- TDD aplicado: pruebas de contrato definidas antes de implementar
- Uso de IA registrado en PROMPTS.md