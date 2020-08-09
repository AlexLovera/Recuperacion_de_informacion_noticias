import unittest
from src.App import *
from src.Recolector_de_noticias import *
from src.Crear_indice_post_list import *
from src.Busqueda import *
from  src.Indice_invertido_y_compresion import *
import shelve

from src.Crear_indice_post_list import _merge_indices,UncompressedPostings,sacar_tildes_y_puntuacion


class Test_Recolector_de_Noticias(unittest.TestCase):

    # def test_probar_que_crea_indice_con_posting_list(self):
    #     with self.assertRaises(KeyError):
    #         #Ingreso direccion invalida
    def test_probar_merge_de_dos_indices_intermedios_desde_disco(self):
        with shelve.open("../Indices_intermedios/indice_intermedio_2", "r") as archivo1,shelve.open("../Indices_intermedios/indice_intermedio_3", "r") as archivo2:
            indice1=archivo1["indice_n°2"]
            indice2=archivo2["indice_n°3"]
            print("1°Indice a mergear",indice1)
            print("2°Indice a mergear",indice2)
            print("indice_final",_merge_indices(indice1, indice2))

    def test_probar_merge_de_dos_indices_intermedios_inventados(self):
        codificador=UncompressedPostings()
        indice1={1:codificador.encode([1,2,3,4,5]),2:codificador.encode([2,4,6,8,10])}
        indice2={1:codificador.encode([11,22,33,44,55]),2:codificador.encode([12]),3:codificador.encode([30,31,32])}
        primer_posting_list_descomprimida=codificador.decode(_merge_indices(indice1, indice2)[1])
        posting_list_esperada=[1,2,3,4,5,33,11,44,22,55]
        self.assertEqual(primer_posting_list_descomprimida,posting_list_esperada)

    def test_probar_quitar_tilde_de_una_palabra(self):
        self.assertEqual(sacar_tildes_y_puntuacion("CompOsición"),"composicion")

    def test_probar_clase_UncompressedPostings(self):
        codificador_de_lista_a_bytearray=UncompressedPostings()
        lista_sin_codificar=[1,15,32,54,2,89,7,12,6,45]
        lista_codificada=codificador_de_lista_a_bytearray.encode(lista_sin_codificar)
        lista_decodificada=codificador_de_lista_a_bytearray.decode(lista_codificada)
        lista_codificada2 = Variable_byte_encode_list(lista_sin_codificar)
        self.assertEqual(lista_decodificada,lista_sin_codificar)

    def test_probar_diferencias_entre_codificaciones(self):
        codificador_de_lista_a_bytearray=UncompressedPostings()
        lista_sin_codificar=[1,15,32,54,2,89,7,12,6,45]
        lista_codificada_a_bitearray=codificador_de_lista_a_bytearray.encode(lista_sin_codificar)
        lista_codificada_con_VB = Variable_byte_encode_list(lista_sin_codificar)
        self.assertNotEqual(lista_codificada_a_bitearray,lista_codificada_con_VB)

    def test_probar_Variable_byte_code(self):
        lista_sin_codificar=[1,15,32,54,2,89,7,12,6,45]
        lista_codificada=Variable_byte_encode_list(lista_sin_codificar)
        lista_decodificada=Variable_byte_decode_list(lista_codificada)
        self.assertEqual(lista_decodificada,lista_sin_codificar)
    # def test_probar_que_crea_indice_con_posting_list(self):
    #     indice=BSBI_algorithm("Medios_prueba")

if __name__ == '__main__':
    unittest.main()