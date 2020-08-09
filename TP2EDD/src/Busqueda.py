import re
import os
import xml.etree.ElementTree as xml
import json
import shelve
from nltk.stem import SnowballStemmer #Stemmer
from colorama import init,Style;init()
from nltk.stem.wordnet import WordNetLemmatizer #Lematizador
from Crear_indice_post_list import UncompressedPostings,sacar_tildes_y_puntuacion
from Indice_invertido_y_compresion import crear_indice_invertido,Variable_byte_decode_list,revertir_saltos_docID

color_error="\033[4;31m"+ Style.BRIGHT
codificador=UncompressedPostings()

def _buscar_e_imprimir_noticia_de_doc(ruta_doc,palabra):
    try:
        tree_archivo = xml.parse(f"Medios/{ruta_doc}")
        root_archivo = tree_archivo.getroot()
        for item in root_archivo.findall('.//item'):
            titulo=item.find('title')
            if not titulo is None:#comprobacion innecesaria?
                if not re.search(palabra,titulo.text.lower()) is None:#si no es nulo, es porque encontro una coincidencia
                    if not item.find('pubDate') is None:#
                        titulo=titulo.text.strip('\n')
                        fecha=item.find('pubDate').text.strip('\n')
                        print(f"{ruta_doc} {titulo} {fecha}")#printea lo necesario
    except xml.ParseError as e:
        print(color_error+f"Error al parsear: Medios/{ruta_doc}")

def busqueda_booleana(palabras,ruta):#REALIZAR PROCESAMIENTO LINGUISTICO SOBRE TODAS LAS PALABRAS
    spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
    lista_de_palabras=[spanish_stemmer.stem(sacar_tildes_y_puntuacion(palabra)) for palabra in palabras.split()]
    lista_de_palabras.sort()
    indice_invertido=dict()
    if not os.path.exists("indice_invertido_pos"):#si no existe tengo que crearlo...
        print("Se debe crear el indice_invertido, aguarde 10 segundos.")
        indice_invertido=crear_indice_invertido(ruta,True)
    else:
        with open("indice_invertido_pos","r") as archivo:
            print("---------INDICE RECUPERADO----------")
            #al recuperar el indice, las claves pasan a ser string
            indice_invertido_str=json.load(archivo)
            for x in indice_invertido_str.keys():
                indice_invertido[int(x)]=indice_invertido_str[x]
    with shelve.open("Dics_mapeo/dic_de_mapeo","r") as dic_term:
        dic_terms_IDS=dic_term["Terminos_ID"]
        dic_docs_IDS=dic_term["Documentos_ID"]
    with open("posting_list_comprimida", "rb") as archivo:#arroja fileNotFound
        for palabra in lista_de_palabras:
            if palabra in dic_terms_IDS:
                termID=dic_terms_IDS[palabra]#esto da el termID
                posicion_inicial=indice_invertido[termID][0]
                if termID+1 in indice_invertido:
                    posicion_final=indice_invertido[termID+1][0]
                archivo.read(posicion_inicial)#paso por encima todos las posting list que no sean necesarias
                posting_list=Variable_byte_decode_list(archivo.read(posicion_final-posicion_inicial))#leo toda la posting list del termID
                # posting_list=revertir_saltos_docID(posting_list)
                print(f"La palabra '{palabra}'', fue encontrada en:")
                for docIDi in posting_list:
                    if  docIDi in dic_docs_IDS:
                        doc=dic_docs_IDS[docIDi]
                        _buscar_e_imprimir_noticia_de_doc(doc,palabra)
            else:
                print(f"'{palabra}' no se encuentra en las noticias")
                import time
                time.sleep(5)