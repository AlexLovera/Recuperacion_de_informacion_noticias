import time;import configparser
from colorama import init,Style;init()
import os
from datetime import datetime
from Excepciones import *
color_error="\033[4;31m"+ Style.BRIGHT
color_blanco='\033[0;37m'
def ejecutar_recolector(config):
    if not config[-4:] == ".ini":
        raise Tipo_de_archivo_incorrecto_exception(config)
    if not os.path.exists(config):
        raise FileNotFoundError
    from Recolector_de_noticias import recolectar_articulos_segun_config
    ruta_medios=input("Ingrese el path de la carpeta con los Medios: ")
    try:
        configuracion = configparser.ConfigParser()
        configuracion.read(config)
        tiempo_espera_entre_ejecuciones=configuracion["DEFAULT"]["query_interval"]
        while True:
            recolectar_articulos_segun_config(ruta_medios,config)
            print(f"Articulos guardados. {datetime.now().hour}:{datetime.now().minute}")
            time.sleep(int(tiempo_espera_entre_ejecuciones))#10 minutos   300=5 min
    except configparser.MissingSectionHeaderError:
        print(color_error+"Archivo mal formado.Asegurese de que este dividido en secciones, con 'DEFAULT' incluida"+color_blanco)
    except KeyboardInterrupt:
        print(color_error+"Se cerrará el programa")
        time.sleep(5)
    except KeyError:
        print(color_error+ 'Asegurese de que el archivo tenga el apartado "query_interval"')
        print("Volverá al menú principal."+color_blanco)
        main()
def ejecutar_opciones(opcion_elegida):
    if opcion_elegida == 1:
        print(color_blanco+"Presione Ctrl+C para detener la recoleccion de articulos en cualquier momento")
        ruta_config=input("Introduzca la ruta de la configuracion(debe contener intervalo de tiempo, url base y direcciones de rss, ext ini):\n")
        try:
            ejecutar_recolector(ruta_config)
        except Tipo_de_archivo_incorrecto_exception as e:
            print(e)
        except Directorio_no_encontrado as e:
            print(e)
        except FileNotFoundError:
            print(color_error+f"El archivo {ruta_config} no fue encontrado."+color_blanco)
    elif opcion_elegida == 2:#se va a dar a elegir si crear indice con compresion o sin
        from Indice_invertido_y_compresion import crear_indice_invertido
        ruta_canales=input("Introduzca la ruta donde se encuentran los canales, para crear indice y luego invertir: ")
        compresion=input("Introduzca 'si o no' en caso de querer un indice comprimido: ")
        if compresion.lower() == "si":
            crear_indice_invertido(ruta_canales,True)
        elif compresion.lower() == "no":
            crear_indice_invertido(ruta_canales,False)
        else:
            raise Opcion_incorrecta_exception(compresion,"si-no")
        print("Indice invertido creado")
    elif opcion_elegida == 3:
        from Busqueda import busqueda_booleana
        palabras_a_buscar=input("Ingrese las palabras a buscar, separadas por un espacio: ")
        ruta_canales=input("Introduzca la ruta donde se encuentran los canales, para crear indice en caso de que no exista: ")
        busqueda_booleana(palabras_a_buscar,ruta_canales)
    else:
        raise Opcion_incorrecta_exception(opcion_elegida,"1-2-3")

def main():
    try:
        #switch case...
        opcion_elegida=int(input("Escriba el numero de la funcion a utilizar:\n1-Recolectar Noticias.\n2-Crear indice "
                                 "invertido con compresion o no.\n3-Realizar busqueda de palabras.\n"))
        try:
            ejecutar_opciones(opcion_elegida)
            utilizar_otra_funcion=input("En caso de querer utilizar otra funcion, introduzca 'si', cualquier cosa en caso contrario: ")
            if utilizar_otra_funcion.lower() == "si":
                main()
        except Opcion_incorrecta_exception as e:
            print(e)
        print(color_blanco)
        utilizar_otra_funcion=input("En caso de querer utilizar otra funcion, introduzca 'si', cualquier cosa en caso contrario: ")
        if utilizar_otra_funcion.lower() == "si":
            main()
    except ValueError:
        print(color_error + "Debe ingresar un entero para elegir una Opcion"+color_blanco)
        main()

if __name__=="__main__":
    main()#ejecutar_app directamente

# #para probar alguna url en particular, titulos nuevos
# tree = xml.parse(request.urlopen("https://www.telam.com.ar/rss2/sociedad.xml"))
# root = tree.getroot()
# for item in root.findall('./channel/item'):
#     print(item.find('title').text)
# time.sleep(60)