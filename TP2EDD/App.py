import time;import configparser
from colorama import init,Style;init()
# from Recolectar_noticias import recolectar_articulos_segun_config
from datetime import datetime
# from Busqueda import busqueda_booleana
# from Indice_invertido_y_compresion import crear_indice_invertido

color_error="\033[4;31m"
color_blanco='\033[0;37m'
def ejecutar_recolector(config):
    from Recolector_de_noticias import recolectar_articulos_segun_config
    try:
        configuracion = configparser.ConfigParser()
        configuracion.read(config)
        tiempo_espera_entre_ejecuciones=configuracion["DEFAULT"]["query_interval"]
        while True:
            recolectar_articulos_segun_config(config)
            print(f"Articulos guardados. {datetime.now().hour}:{datetime.now().minute}")
            time.sleep(int(tiempo_espera_entre_ejecuciones))#10 minutos   300=5 min
    except KeyboardInterrupt:
        print(color_error+"Se cerrara el programa")
        time.sleep(5)
    except KeyError:
        print(color_error + Style.BRIGHT + 'Asegurese de que ingreso la ruta del archivo config y que tenga el apartado "query_interval"')
        print("Volverá al menú principal.")
        # time.sleep(5)
        main()
def ejecutar_opciones(opcion_elegida):
    if opcion_elegida == 1:
        print(color_blanco+"Presione Ctrl+C para detener la recoleccion de articulos en cualquier momento")
        ruta_config=input("Introduzca la ruta de la configuracion(debe contener intervalo de tiempo, url base y direcciones de rss, ext ini):\n")
        ejecutar_recolector(ruta_config)
    elif opcion_elegida == 2:#se va a dar a elegir si crear indice con compresion o sin
        from Indice_invertido_y_compresion import crear_indice_invertido
        ruta_canales=input("Introduzca la ruta donde se encuentran los canales, para crear indice y luego invertir: ")
        compresion=input("Introduzca 'si o no' en caso de querer un indice comprimido: ")
        if compresion.lower() == "si":
            crear_indice_invertido(ruta_canales,True)
        elif compresion.lower() == "no":
            crear_indice_invertido(ruta_canales,False)
        else:
            raise Exception#hacer una propia
    elif opcion_elegida == 3:
        from Busqueda import busqueda_booleana
        palabras_a_buscar=input("Ingrese las palabras a buscar, separadas por un espacio: ")
        ruta_canales=input("Introduzca la ruta donde se encuentran los canales, para crear indice en caso de que no exista: ")
        busqueda_booleana(palabras_a_buscar,ruta_canales)
        time.sleep(15)
    else:
        raise Exception#hacer excepcion propia par opcion incorrecta

def main():
    try:
        #switch case...
        opcion_elegida=int(input("Escriba el numero de la funcion a utilizar:\n1-Recolectar Noticias.\n2-Crear indice "
                                 "invertido con compresion o no.\n3-Realizar busqueda de palabras.\n"))
        ejecutar_opciones(opcion_elegida)
        utilizar_otra_funcion=input("En caso de querer utilizar otra funcion, introduzca 'si', cualquier cosa en caso contrario: ")
        if utilizar_otra_funcion.lower() == "si":
            main()
    except ValueError:
        print("\033[4;31m" + Style.BRIGHT + "Debe ingresar un entero para elegir una Opcion")
        time.sleep(5)

if __name__=="__main__":
    main()#ejecutar_app directamente

# #para probar alguna url en particular, titulos nuevos
# tree = xml.parse(request.urlopen("https://www.telam.com.ar/rss2/sociedad.xml"))
# root = tree.getroot()
# for item in root.findall('./channel/item'):
#     print(item.find('title').text)
# time.sleep(60)