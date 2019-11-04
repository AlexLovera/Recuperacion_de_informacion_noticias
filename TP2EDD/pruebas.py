# # import string
# # def acondicionar_palabra(pal):
# #     reemplazos = (("á", "a"), ("é", "e"), ("ó", "o"), ("ú", "u"))
# #     pal = pal.lower()
# #     pal = pal.strip()
# #     pal = pal.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
# #     for a, b in reemplazos:
# #         pal = pal.replace(a, b)
# #     return pal
# # def crear_lista_a_partir_de_string():
# #     a = "No sabemos cuándo empezó Tolkien a dirigir sus pensamientos al Reino"
# #     lista_palabras=[acondicionar_palabra(palabra) for palabra in a.split()]
# #     print(lista_palabras)
# #     print(type(lista_palabras))
# #     return lista_palabras
# #
# # # lista=crear_lista_a_partir_de_string()
# # # lista.sort()
# # # print(lista)
# #
# # def dic():
# #     dic=dict()
# #     dic.setdefault("hola",(2,3))
# #     print(dic)
# # dic()
# import xml.etree.ElementTree as xml
# def comprobar_repetidos():
#     arbol = xml.parse('Medios/La Voz/últimas noticias.xml')
#     hijo = arbol.getroot()
#     lista=list()
#     es=0
#     for item in arbol.findall('.//item'):
#         titulo=item.find('title').text
#         fecha=item.find('pubDate').text
#         # titulo=titulo.replace(" ","")
#         # fecha=fecha.replace(" ","")
#         print(titulo.replace(" ",""))
#         # if es == 0:
#         lista.append(titulo+fecha)
#         es+=1
#         esta=titulo+fecha in lista
#         x=0
#
# comprobar_repetidos()
# import json#guardar varias listas es posible
# # lista=[1,2,"hola",3]
# # lista2=["x","y","chau","z","x"]
# dic={"hola":"primero","chau":"ultimo"}
# dic2={"a":1,"b":2}
# with open("prueba_serializado.json", "a") as archivo:
#     json.dump(dic, archivo)
#     lista=json.load(archivo)
#     lista.append(lista2)
#     print(lista)
#     with open("prueba_serializado.json", "w") as archivo:
#         json.dump(lista, archivo)
#     # json.dump(lista,archivo)
#     # json.dump(lista2,archivo)

############LEMATIZADOR CON DIC DE GITHUB
# encoding: utf8
# lemmaDict = {}
# with open('lemmatization-es.txt', 'rb') as f:
#     data = f.read().decode('utf8').replace(u'\r', u'').split(u'\n')
#     data = [a.split(u'\t') for a in data]
#
# for a in data:
#     if len(a) > 1:
#         lemmaDict[a[1]] = a[0]
#
#
# def lemmatize(word):
#     return lemmaDict.get(word, word + u'*')

# from nltk import word_tokenize #Tokenizer, instalar... inutil? stanfordTokenizer?
# from nltk.stem import SnowballStemmer #Stemmer
# from nltk.corpus import stopwords #Stopwords
# from nltk.stem.wordnet import WordNetLemmatizer #Lematizador
# lematizador = WordNetLemmatizer()
# stop_words = set(stopwords.words('spanish'))#lista de stop words
# spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=True)
# # print(spanish_stemmer.stem('cuando'))
# text = 'En su parte de arriba encontramos la zona de mandos, donde se puede echar el detergente, aunque en nuestro caso lo al ser gel lo ponemos directamente junto con la ropa.'
# text_sin_stop_words = [spanish_stemmer.stem(lematizador.lemmatize(w)) for w in text.split() if not w in stop_words]#agrego funcion a w, lematizo
# print(text_sin_stop_words)

# stemmed_text =  [spanish_stemmer.stem(word) for word in text.split()]
# print(len(stemmed_text))
# print(stemmed_text)
# print(spanish_stemmer.stopwords)
# stemmed_text = [spanish_stemmer.stem(i) for i in word_tokenize(text)]#falta algo





# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer("spanish")
# print(stemmer.stem('cuando'))
import array


class UncompressedPostings:

    @staticmethod
    def encode(postings_list):
        """Encodes postings_list into a stream of bytes

        Parameters
        ----------
        postings_list: List[int]
            List of docIDs (postings)

        Returns
        -------
        bytes
            bytearray representing integers in the postings_list
        """
        return array.array('L', postings_list).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        """Decodes postings_list from a stream of bytes

        Parameters
        ----------
        encoded_postings_list: bytes
            bytearray representing encoded postings list as output by encode
            function

        Returns
        -------
        List[int]
            Decoded list of docIDs from encoded_postings_list
        """

        decoded_postings_list = array.array('L')
        decoded_postings_list.frombytes(encoded_postings_list)
        return decoded_postings_list.tolist()
#
codificador=UncompressedPostings()
lista_codificada=codificador.encode([1,2])
# conjunto_codificado=set()
# conjunto_codificado.add(1)
# conjunto_codificado.add(2)
# conjunto_codificado=codificador.encode(conjunto_codificado)
# print(lista_codificada)
# print(conjunto_codificado)
# print("deberia de ser un conjunto:" ,type(set(codificador.decode(conjunto_codificado))))
# dic=dict()
# dic[1]=conjunto_codificado
# dic[2]=lista_codificada
# import json
# import pickle
# import shelve
# # def cargar_bytearray():
# #     with open("indice_intermedio_CLARÍN", "r") as archivo:
# #         dic = pickle.load(archivo)
# #     print(dic)
# def guardar_dic_bytearray():
#     with open("indice_intermedio_CLARÍN2", "wb") as archivo:
#         pickle.dump(dic,archivo)
# # guardar_dic_bytearray()
# def cargar_bytearray():
#      with open("indice_intermedio_CLARÍN2", "rb") as archivo:
#          dic = pickle.load(archivo)
#      print(dic)
#      return dic
# dicb=cargar_bytearray()
# dic2=cargar_bytearray()
# dic3=dict()
# dic3[3]=codificador.encode([1,2,3])
# dic3[2]=codificador.encode([4,5,6])#agrego a este dic para ver si mergea los dic con bytearray
# print(dic3,"dic3")
# def guardar_como_shelve():
#     #guardo con shelve, los dos diccionarios, asignandole claves arbitrariamente.En un solo archivo
#     with shelve.open('shelf-example',"c") as db:
#         db["primer_indice"] = dic
#         db["segundo_indice"] = dic2
# guardar_como_shelve()
# def cargar_shelve():
#     #cargo desde shelve, la clave y valor, guardados
#     print("cargo desde shelve, la clave y valor, guardados")
#     with shelve.open('shelf-example', 'r') as shelf:
#         for key in shelf.keys():
#             print(key,shelf[key])
# cargar_shelve()
# dicb.update(dic3)#mergea mal, se come la primer lista que estaba en dic[2]
# print(dicb)
# import queue
# # def cola_prioridad_imprimir():
# #     for clave in dic:
# #         cola_prioridad_terminos=queue.PriorityQueue()
# #         cola_prioridad_terminos.join(clave)
# #     print("cola de prioridad",cola_prioridad_terminos)
# # cola_prioridad_imprimir()
# # cola=queue.Queue()
# # cola.put(5)
# # cola.put(3)
# # cola.put(9)
# # cola.put(4)
# # cola_de_keys=queue.Queue(list(dicb.keys()))
# # print(cola_de_keys.get())
# # print(cola_de_keys.get())
# lista_como_cola=[1,5,4,3,10]
# # print(lista_como_cola.)
# import math
# print(math.ceil(2.5))
# print(lista_como_cola[-1])
# diccc=dict()
# diccc["hola"]=lista_codificada
# print("diccccc",diccc)
# with open("hola","wb") as archivo:
#     archivo.writelines(lista_codificada)
num_bloque=2
for x in range(0,5,2):
    print(x)

# import sys
# print(lista_codificada)
# print("tamaño en bytes, lista de doc: ",sys.getsizeof(lista_codificada))
# peso_de_lista_bytes=0
# with open("prueba_bytes","wb") as archivo:
#     archivo.write(lista_codificada)
#     print("posicion_luego_de_escribir: ",archivo.tell())
#     archivo.write(codificador.encode([1,2,3,5,4,6,8,9,10]))
#     # archivo.writelines([lista_codificada,codificador.encode([1,2,3,5,4,6,8,9,10])])
#     peso_de_lista_bytes=sys.getsizeof(lista_codificada)
#     print("peso_de_lista_bytes: ",peso_de_lista_bytes)
#
# with open("prueba_bytes","rb") as archivo:
#     posicion_inicial=archivo.tell()
#     lista_cod_recuperada=archivo.read(8)
#     posicion_final=archivo.tell()
#     print("posicion inicial: ",posicion_inicial)
#     print("posicion final: ",posicion_final)
#     # print(archivo.read())
#     print("lista_cod_recuperada: ",lista_cod_recuperada)

# dic={"x":("hola",1,3),"y":("chau",2,4)}
# print(dic["x"][2])
stringg="no puede ser, tenia chau"#voy a tener que usar expresiones regulares, ya que lo toma mal
print("ten" in stringg)
import xml.etree.ElementTree as xml
def imprimir_titulos():
    tree_archivo = xml.parse("Medios/CLARÍN/autos.xml")
    root_archivo = tree_archivo.getroot()
    for item in root_archivo.findall('.//item'):
        print(item.find('title').text)
        # titulo = item.find('title')
        # if not titulo is None:
        #     print(titulo.text)
imprimir_titulos()
