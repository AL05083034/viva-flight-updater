import unittest

def validar_estado_esperado(estado):
    """Función de prueba para simular la validación del estado del vuelo."""
    return estado.lower() == "active"

class TestVuelos(unittest.TestCase):
    def test_validacion_estado(self):
        # Esta prueba siempre será exitosa porque le estamos mandando "active"
        self.assertTrue(validar_estado_esperado("active"))

if __name__ == '__main__':
    unittest.main()