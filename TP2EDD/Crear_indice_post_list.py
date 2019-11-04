import json
import shelve
import array
import os
from nltk.stem import SnowballStemmer #Stemmer
from nltk.corpus import stopwords #Stopwords
from nltk.stem.wordnet import WordNetLemmatizer #Lematizador
import math
import pickle
import sys
import queue#usar Queue o SimpleQueue
import xml.etree.ElementTree as xml
import string

def _guardar_indices_intermedios_o_dic(ruta,indice,numero_de_bloque=0,indice2=None):
    with shelve.open(ruta, "c") as archivo:
        if numero_de_bloque is 0:#si es 0 es porque voy a guardar dic de term o doc, mapeo
            archivo["Terminos_ID"] = indice
            archivo["Documentos_ID"] = indice2
        else:
            archivo[f"indice_n°{numero_de_bloque}"] = indice

class UncompressedPostings:

    @staticmethod
    def encode(postings_list):
        return array.array('L', postings_list).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        decoded_postings_list = array.array('L')
        decoded_postings_list.frombytes(encoded_postings_list)
        return decoded_postings_list.tolist()

def acondicionar_palabra(palabra):
    reemplazos = (("á", "a"), ("é", "e"), ("ó", "o"), ("ú", "u"))
    palabra = palabra.lower()
    palabra = palabra.strip()
    palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
    for a, b in reemplazos:
        palabra = palabra.replace(a, b)
    return palabra

def _merge_indices_intermedios(cant_bloques,lista_merge_de_indices=None,lista_indices=None):
    # bloques_1=cant_bloques is 1#lo toma como False
    if cant_bloques == 1 and not (lista_indices is None):#si me dan un solo bloque al comienzo? arreglar
        return lista_indices
    if lista_merge_de_indices is None:
        lista_merge_de_indices=list()
    # return _merge_indices(lista_indices[0],lista_indices[1])
    while cant_bloques>1:
        for bloque in range(0,cant_bloques,2):
            # print("n°bloque: ",bloque,bloque+1)
            try:
                indice_fusionado=_merge_indices(lista_indices[bloque],lista_indices[bloque+1])
            except Exception:
                print("n°bloque: ", bloque, bloque + 1)
                print("longitud de lista: ",len(lista_indices))
            # print("indice_fusionado: ",indice_fusionado)
            lista_merge_de_indices.append(indice_fusionado)
        cant_bloques=math.ceil(cant_bloques/2)#redondea para arriba
        # if cant_bloques is 1:
        #     lista_merge_de_indices.append(lista_indices[-1])
        return _merge_indices_intermedios(cant_bloques,lista_indices=lista_merge_de_indices)

def _merge_indices(indices_invertidos_intermedios,indices_invertidos_intermedios2):
    indice_invertido_final=dict()
    keys_indice1=queue.Queue()
    keys_indice2=queue.Queue()
    keys_ordenadas1=list(indices_invertidos_intermedios.keys());keys_ordenadas1.sort()
    keys_ordenadas2=list(indices_invertidos_intermedios2.keys());keys_ordenadas2.sort()
    for key in keys_ordenadas1: keys_indice1.put(key)
    for key in keys_ordenadas2: keys_indice2.put(key)
    termID1 = keys_indice1.get()
    termID2 = keys_indice2.get()
    while (not keys_indice1.empty()) or (not keys_indice2.empty()):
        if keys_indice1.empty():#relleno el indice con estos datos#es O(1) el metodo, o deberia
            termID2=keys_indice2.get()
            indice_invertido_final[termID2] = indices_invertidos_intermedios2[termID2]
        elif keys_indice2.empty():
            termID1 = keys_indice1.get()
            indice_invertido_final[termID1] = indices_invertidos_intermedios[termID1]
        else:
            if termID1 == termID2:
                indice_invertido_final[termID1]=codificador.encode(set(codificador.decode(indices_invertidos_intermedios[termID1]))| set(codificador.decode(indices_invertidos_intermedios2[termID2])))
                termID1 = keys_indice1.get()#Desencolo los dos
                termID2 = keys_indice2.get()
            elif termID1<termID2:
                indice_invertido_final[termID1]=indices_invertidos_intermedios[termID1]
                termID1 = keys_indice1.get()
            else:
                indice_invertido_final[termID2]=indices_invertidos_intermedios2[termID2]
                termID2 = keys_indice2.get()
    return indice_invertido_final

codificador=UncompressedPostings()

def BSBI_algorithm(ruta):#ruta=Medios
    lematizador = WordNetLemmatizer()
    stop_words = set(stopwords.words('spanish'))  # lista de stop words
    spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
    docID=0
    termID = 0
    dic_termino_termID=dict()#guardar en DISCO
    dic_documentos_ID=dict()#guardar en DISCO
    numero_de_bloque=0
    for medio in os.listdir(ruta):#medios
        dic_term_posting=dict()
        numero_de_bloque+=1
        dic_por_termID_postL = dict()#este sera el nuevo indice para el bloque
        for arch_xml in os.listdir(ruta+"/"+medio):
            #termino:postinList
            docID += 1
            #print(arch_xml,docID)
            # dic_documentos_ID[medio+">"+arch_xml]=docID#guardar en DISCO
            dic_documentos_ID[docID]=medio+"/"+arch_xml
            tree=xml.parse(ruta+"/"+medio+"/"+arch_xml)
            root=tree.getroot()
            for item in root.findall('.//item'):
                titulo=item.find('title')
                if not titulo is None:
                    titulo = titulo.text
                    # titulos_juntos+=" "+titulo#para que no se junten la primera y ultima palabra de los titulos
        #Hasta aca tengo que tener todos los titulos en un string
        #Primero le saco las tildes, puntuacion, verifico que no este en las stop_words y luego stemming, lemat...
                    lista_palabras = [acondicionar_palabra(palabra) for palabra in titulo.split() if not palabra in stop_words]#para ordenar
                    lista_palabras=[spanish_stemmer.stem(lematizador.lemmatize(w)) for w in lista_palabras]
                    # lista_palabras.sort()#titulo ordenado alfabeticamente
                    for palabra in lista_palabras:#creo dic_term_posting
                        dic_term_posting.setdefault(palabra, set())
                        dic_term_posting[palabra].add(docID)
        palabras_ordenadas=list(dic_term_posting.keys())
        palabras_ordenadas.sort()
        for palabra in palabras_ordenadas:
            if palabra not in dic_termino_termID:  # hago esto porque solo tiene que agregar el termID una vez
                termID += 1
                dic_termino_termID[palabra]=termID#palabra: termID
                #En caso de que este...
            termID_actual=dic_termino_termID[palabra]
            dic_por_termID_postL.setdefault(termID_actual,codificador.encode(dic_term_posting[palabra]))
        _guardar_indices_intermedios_o_dic(f"Indices_intermedios/indice_intermedio_{numero_de_bloque}",dic_por_termID_postL,numero_de_bloque)
    #Merge de bloques a un indice grande
    _guardar_indices_intermedios_o_dic("Dics_mapeo/dic_de_mapeo",dic_termino_termID,0,dic_documentos_ID)#guardo mapeos
    del dic_termino_termID;del dic_documentos_ID;del dic_por_termID_postL
    #Ir leyendo indices intermedios y pasarlos de a poco para no leer todos de una. LEO 2 Y BORRO VARIABLES
    lista_indices=list()
    for numB in range(1,numero_de_bloque+1):
        with shelve.open(f"Indices_intermedios/indice_intermedio_{numB}", "rb") as archivo:
            for bloque in archivo:
                lista_indices.append(archivo[bloque])
    # print(lista_indices)
    # print(numero_de_bloque)
    posting_list=_merge_indices_intermedios(numero_de_bloque, lista_indices=lista_indices)
    print(posting_list[0])
    with open("posting_list","wb") as archivo:
        pickle.dump(posting_list[0],archivo)
    del lista_indices
    return posting_list[0]

# def generar_saltos_docID(post_list_prueba,ruta_creacion_posting_list=None,ruta_posting_list=None):
#     # if ruta_creacion_posting_list is None and ruta_posting_list is None:
#     #     #raise #se tiene que agregar alguna ruta...
#     #     pass
#     post_list_comprimida=dict()
#     if ruta_posting_list is None:#creo la posting_list
#         # posting_list_sin_comprimir = BSBI_algorithm(ruta_creacion_posting_list)
#         posting_list_sin_comprimir=post_list_prueba
#         #de aca para abajo se podria sacar del if? total se tiene que hacer en los dos casos en los que se resuelva
#         for termIDi in posting_list_sin_comprimir:
#             post_list_comprimida.setdefault(termIDi,list())
#             term_post_list=posting_list_sin_comprimir[termIDi]# le pido la postin list propia del termino
#             for docIDi in range(len(posting_list_sin_comprimir[termIDi])):
#                 if docIDi == 0:
#                     post_list_comprimida[termIDi].append(posting_list_sin_comprimir[termIDi][docIDi])
#                 else:
#                     #aca le resto el valor previo en la lista de apariciones...
#                     post_list_comprimida[termIDi].append(posting_list_sin_comprimir[termIDi][docIDi]-posting_list_sin_comprimir[termIDi][docIDi-1])
#     else:
#         #recuperar posting list de disco, pasar keys a int? y ahi trabajarlo
#         pass
#     return post_list_comprimida
#
#
# def crear_indice(ruta,posting_list_comprimida):#ruta y boolean
#     indice_final = dict()
#     if posting_list_comprimida:#supongo que lo tengo que escribir, lista comprimida?
#         posting_list = BSBI_algorithm(ruta)
#         with open("posting_list_comprimida","wb") as archivo:
#             for termIDi in posting_list:
#                 lista_docs=posting_list[termIDi]
#                 indice_final[termIDi]=(archivo.tell(),len(codificador.decode(lista_docs)),sys.getsizeof(lista_docs))
#                 archivo.write(lista_docs)
#         print("indice_final_posting_comprimida: ",indice_final)
#     else:
#         posting_list = BSBI_algorithm(ruta)
#         for termIDi in posting_list:
#             lista_decodificada = codificador.decode(posting_list[termIDi])
#             indice_final[termIDi] = (termIDi, len(lista_decodificada), sys.getsizeof(lista_decodificada))
#         print(indice_final)
#     with open("indice_invertido_pos","w") as archivo:
#         json.dump(indice_final,archivo)
#     return indice_final

# x=BSBI_algorithm("Medios_prueba")
#ser/macri/messi/hoy/que/ley/militar/ten?
#VER sanchez, que no imprime titulos, pero si posting list

#Funciona lo de abajo, prueba... agregando una posting list vacia y comentando el primer if y bsbi
# post_list_prueba={1:[7,25,43,104,105],2:[8,16,30,100,106]}
# print(generar_saltos_docID(post_list_prueba))