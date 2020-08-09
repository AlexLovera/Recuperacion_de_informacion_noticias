import xml.etree.ElementTree as xml
import configparser
import os.path
from colorama import init,Style;init()
import requests
from Excepciones_TP2 import Tipo_de_archivo_incorrecto_exception,Directorio_no_encontrado
color_error="\033[4;31m"+ Style.BRIGHT
color_blanco='\033[0;37m'
def _compara_xmls_y_añade_articulos_nuevos(url,xmlfile):
    # print(url)#debuggear, porque se "trababa", el problema es que la pagina tardaba en responder, y despues se cayo
    try:
        resp = requests.get(url,timeout=4)
        resp.encoding = 'utf-8'
        tree_url = xml.fromstring(resp.text)
    # tree_url=xml.fromstring(resp.text)
        tree_archivo = xml.parse(xmlfile)
        root_archivo = tree_archivo.getroot()
        lista_titulo_y_fecha_xml = list()
        # voy a recorrer el xml y guardar titulo y fecha en un string para comprobar que no haya repetidas luego
        for item in root_archivo.findall('.//item'):
            titulo=item.find('title')
            fecha=item.find('pubDate')
            if not titulo is None and not fecha is None:
                lista_titulo_y_fecha_xml.append(titulo.text.replace(" ","") + fecha.text.replace(" ",""))
            else:
                fecha=item.find('dc:date')
                if not titulo is None and not fecha is None:
                    lista_titulo_y_fecha_xml.append(titulo.text.replace(" ", "") + fecha.text.replace(" ", ""))
    #####################################
        for item in tree_url.findall('.//item'):
            if not item.find('title') is None and not item.find('pubDate') is None:#La voz tiene problema con los espacios
                titulo_y_fecha_xml = item.find('title').text.replace(" ","") + item.find('pubDate').text.replace(" ","")
                if not titulo_y_fecha_xml in lista_titulo_y_fecha_xml:
                    root_archivo.find('channel').append(item)
            elif not item.find('title') is None and not item.find('dc:date') is None:
                titulo_y_fecha_xml = item.find('title').text.replace(" ","") + item.find('dc:date').text.replace(" ","")
                if not titulo_y_fecha_xml in lista_titulo_y_fecha_xml:
                    root_archivo.find('channel').append(item)
        tree_archivo.write(xmlfile,encoding="utf-8")
    except requests.Timeout:
        print(color_error+"Se excedio el tiempo para la peticion, url: "+color_blanco,url)
    except Exception as e:
        # print(Exception.with_traceback())
        if "not well-formed" in e.__str__():
            print(color_error+f"Estructura de la pagina mal formada o pagina caida: {url}")
        print(color_error+"Error en: ",url+color_blanco)

def _crear_xml_mediante_config_y_agrega_articulo(carpeta_medios,config):
    if not os.path.isdir(carpeta_medios):#si no existe la carpeta medios devuelvo excepcion propia
        raise Directorio_no_encontrado(carpeta_medios)
    configuracion = configparser.ConfigParser()
    configuracion.read(config)
    cantidad_de_items_a_saltear=len(configuracion.items(configuracion.default_section))
    for medio in configuracion.sections():
        if not os.path.isdir(f"{carpeta_medios}/{medio}"):#si no existe la carpeta para el medio, se la creo
            os.mkdir(f"{carpeta_medios}/{medio}")
        lista_de_tupla_items_de_la_seccion=configuracion.items(medio)
        url_base=str(configuracion[medio]["url_base"])
        numero_de_tupla = 0
        for tupla_de_valores in lista_de_tupla_items_de_la_seccion:
            variable,valor=tupla_de_valores
            numero_de_tupla+=1
            # url_base_como_variable=[k for k, v in configuracion[seccion] if v == medio?]
            if(numero_de_tupla<=cantidad_de_items_a_saltear+1): continue#4#pasa los valores por defecto
            if numero_de_tupla>cantidad_de_items_a_saltear+1: seccion=str(valor)#4
            if not os.path.exists(f"Medios/{medio}/{str(variable) + '.xml'}"):#para saltear los valor default y url
                #si no existe el archivo, lo tengo que crear
                resp = requests.get(url_base + seccion)
                with open(f"Medios/{medio}/{variable + '.xml'}", 'wb') as archivo:
                    archivo.write(resp.content)
            elif os.path.exists(f"Medios/{medio}/{str(variable) + '.xml'}"):
                _compara_xmls_y_añade_articulos_nuevos(url_base + seccion,f"Medios/{medio}/{str(variable) + '.xml'}")

def recolectar_articulos_segun_config(carpeta_medios,config):
    try:
        _crear_xml_mediante_config_y_agrega_articulo(carpeta_medios,config)
    except configparser.ParsingError:
        print('\033[4;31m' + f"No se encontró el archivo a parsear: {config}")
