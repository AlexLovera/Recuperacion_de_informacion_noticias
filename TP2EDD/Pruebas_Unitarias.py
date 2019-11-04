import unittest
from App import ejecutar_app

class Test_Recolector_de_Noticias(unittest.TestCase):

    def test_probar_que_poner_direccion_invalida_lanza_error(self):
        with self.assertRaises(KeyError):
            #Ingreso direccion invalida
            ejecutar_app("mkfpwe")


if __name__ == '__main__':
    unittest.main()