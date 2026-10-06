from django.test import TestCase

class SumaTest(TestCase):
    def test_operacion_suma(self):
        val1 = 15
        val2 = 25
        self.assertEqual(val1 + val2, 40)