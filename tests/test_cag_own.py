"""
Pruebas propias - Miguel Alfonso Dubon 0900-21-6641
BDD/TDD: Verificacion del modulo CAG implementado
"""
import unittest
from backend.context_store import ContextStore
from backend.cag import apply_context


class TestContextStoreUnit(unittest.TestCase):

    def setUp(self):
        self.store = ContextStore()

    def test_save_returns_true(self):
        result = self.store.save("user1", "tema", "redes neuronales")
        self.assertTrue(result)

    def test_list_empty_for_new_user(self):
        result = self.store.list_for_user("nuevo_usuario")
        self.assertEqual(result, [])

    def test_save_and_retrieve_single_item(self):
        self.store.save("user2", "nivel", "avanzado")
        items = self.store.list_for_user("user2")
        self.assertIn({"key": "nivel", "value": "avanzado"}, items)

    def test_save_multiple_keys_same_user(self):
        self.store.save("user3", "idioma", "espanol")
        self.store.save("user3", "nivel", "basico")
        items = self.store.list_for_user("user3")
        self.assertEqual(len(items), 2)

    def test_context_isolated_between_users(self):
        self.store.save("ana", "estilo", "formal")
        self.store.save("bob", "estilo", "informal")
        ana_items = self.store.list_for_user("ana")
        bob_items = self.store.list_for_user("bob")
        self.assertNotEqual(ana_items, bob_items)

    def test_overwrite_existing_key(self):
        self.store.save("user4", "nivel", "basico")
        self.store.save("user4", "nivel", "avanzado")
        items = self.store.list_for_user("user4")
        values = [i["value"] for i in items]
        self.assertIn("avanzado", values)
        self.assertNotIn("basico", values)


class TestApplyContextUnit(unittest.TestCase):

    def test_no_context_returns_base_answer(self):
        answer, used = apply_context("user1", "pregunta", "respuesta base", [])
        self.assertEqual(answer, "respuesta base")
        self.assertEqual(used, [])

    def test_context_enriches_answer(self):
        items = [{"key": "nivel", "value": "principiante"}]
        answer, used = apply_context("user1", "pregunta", "respuesta base", items)
        self.assertIn("principiante", answer.lower())

    def test_context_used_contains_keys(self):
        items = [{"key": "audience", "value": "explicar como principiante"}]
        answer, used = apply_context("user1", "pregunta", "respuesta base", items)
        self.assertIn("audience", used)

    def test_multiple_context_items_all_used(self):
        items = [
            {"key": "nivel", "value": "basico"},
            {"key": "idioma", "value": "espanol"},
        ]
        answer, used = apply_context("user1", "pregunta", "respuesta base", items)
        self.assertIn("nivel", used)
        self.assertIn("idioma", used)


if __name__ == "__main__":
    unittest.main()