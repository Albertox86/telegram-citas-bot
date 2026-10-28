import unittest

from bot.intents import build_default_intent_engine


class TestIntentEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_default_intent_engine()

    def test_detects_appointment_request_spanish(self):
        result = self.engine.detect("Hola, quiero agendar una cita")
        self.assertEqual(result.intent_name, "appointment_request")

    def test_detects_appointment_request_turno(self):
        result = self.engine.detect("Necesito un turno para mañana")
        self.assertEqual(result.intent_name, "appointment_request")

    def test_fallback(self):
        result = self.engine.detect("Gracias por todo")
        self.assertEqual(result.intent_name, "fallback")


if __name__ == "__main__":
    unittest.main()
