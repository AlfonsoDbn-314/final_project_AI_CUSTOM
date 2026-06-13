"""Módulo CAG: aplica contexto persistente del usuario para enriquecer respuestas."""


def apply_context(user_id, question, base_answer, context_items):
    if not context_items:
        return base_answer, []

    context_used = []
    enriched = base_answer

    for item in context_items:
        key = item["key"]
        value = item["value"]
        context_used.append(key)
        enriched = f"{enriched} [{key}: {value}]"

    return enriched, context_used