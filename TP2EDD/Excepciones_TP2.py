from math import sqrt as raiz_cuadrada;
from colorama import init, Style

init()
formato_error = '\033[4;31m'


class Indices_y_busqueda_exception(Exception):
    pass


class Tipo_de_archivo_incorrecto_exception(Indices_y_busqueda_exception):
    """tipo de archivo incorrecto"""

    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada

    def __str__(self):
        return formato_error + Style.BRIGHT+ f"El tipo de archivo indicado como:{self.archivo_entrada}, es incorrecto.Debe " \
            f"ser .ini"

class Opcion_incorrecta_exception(Indices_y_busqueda_exception):
    def __init__(self, opcion,opciones_validas):
        self.opcion=opcion
        self.opciones_validas=opciones_validas
    def __str__(self):
        return formato_error + Style.BRIGHT+ f"Opcion {self.opcion} no es valida.Debe ingresar alguna de las siguientes opciones: {self.opciones_validas}"

class Directorio_no_encontrado(Indices_y_busqueda_exception):
    def __init__(self,nombre_dir):
        self.nombre_dir = nombre_dir
    def __str__(self):
        return formato_error + Style.BRIGHT+ f"No se encontró la carpeta: {self.nombre_dir}"