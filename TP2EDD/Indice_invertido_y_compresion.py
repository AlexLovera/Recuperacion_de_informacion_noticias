import json
import sys
from Crear_indice_post_list import UncompressedPostings,BSBI_algorithm
codificador=UncompressedPostings()
from struct import pack, unpack

def Variable_byte_encode_number(numero):
    bytes_list = []
    while True:
        bytes_list.insert(0, numero % 128)
        if numero < 128:
            break
        numero = numero // 128
    bytes_list[-1] += 128
    return pack('%dB' % len(bytes_list), *bytes_list)

def Variable_byte_encode_list(numeros):
    bytes_list = []
    for number in numeros:
        bytes_list.append(Variable_byte_encode_number(number))
    return b"".join(bytes_list)

def Variable_byte_decode_list(bytestream):
    n = 0
    numbers = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers

def _generar_saltos_docID(indice_sin_comprimir):#MODIFICADO
    indice_con_saltos_docID=dict()
    for termIDi in indice_sin_comprimir:
        indice_con_saltos_docID.setdefault(termIDi,list())
        term_post_list=codificador.decode(indice_sin_comprimir[termIDi])# le pido la postin list propia del termino
        for docIDi in range(len(term_post_list)):
            if docIDi == 0:
                indice_con_saltos_docID[termIDi].append(term_post_list[docIDi])
            else:
                #aca le resto el valor previo en la lista de apariciones...
                indice_con_saltos_docID[termIDi].append(term_post_list[docIDi] - indice_sin_comprimir[termIDi][docIDi - 1])
    print(indice_con_saltos_docID)
    import time
    time.sleep(10)
    return indice_con_saltos_docID

def _comprimir_posting_list(ruta,indice_final):
    # indice_sin_comprimir = BSBI_algorithm(ruta)
    indice_con_saltos_docID=_generar_saltos_docID(BSBI_algorithm(ruta))
    with open("posting_list_comprimida", "wb") as archivo:
            for termIDi in indice_con_saltos_docID:
                lista_docs=indice_con_saltos_docID[termIDi]
                # termi_posting_decodificada=codificador.decode(lista_docs)
                #codifico posting list con Variable byte code
                termi_posting_codificada=Variable_byte_encode_list(lista_docs)
                indice_final[termIDi]=(archivo.tell(),len(termi_posting_codificada),sys.getsizeof(termi_posting_codificada))
                archivo.write(termi_posting_codificada)
    print("indice_final_posting_comprimida: ",indice_final)
    return indice_final


def crear_indice_invertido(ruta,posting_list_comprimida):#ruta y boolean
    indice_final = dict()
    if posting_list_comprimida:#supongo que lo tengo que escribir, lista comprimida?
        indice_final=_comprimir_posting_list(ruta,indice_final)
        # posting_list = BSBI_algorithm(ruta)#ejemplo sin comprimir
        # with open("posting_list_comprimida","wb") as archivo:
        #     for termIDi in posting_list:
        #         lista_docs=posting_list[termIDi]
        #         indice_final[termIDi]=(archivo.tell(),len(codificador.decode(lista_docs)),sys.getsizeof(lista_docs))
        #         archivo.write(lista_docs)
        # print("indice_final_posting_comprimida: ",indice_final)
    else:
        indice_sin_comprimir = BSBI_algorithm(ruta)
        for termIDi in indice_sin_comprimir:
            lista_decodificada = codificador.decode(indice_sin_comprimir[termIDi])
            indice_final[termIDi] = (termIDi, len(lista_decodificada), sys.getsizeof(lista_decodificada))
        print("indice final posting sin comprimir: ",indice_final)
    with open("indice_invertido_pos","w") as archivo:
        json.dump(indice_final,archivo)
    return indice_final

# generar_saltos_docID(ruta_creacion_posting_list="Medios_prueba")
#4251: [19, -19, 0, 0, 23, -23, 0, 0, 165, -165, 0, 0, 41, -41, 0, 0, 42, -42, 0, 0, 171, --171, 0, 0, 172, -172, 0, 0, 45, -45, 0, 0, 175, -175, 0, 0, 177, -177, 0, 0, 179, -179, 0, 0, 180, -180, 0, 0, 181, -181, 0, 0,
# print(codificador.decode(posting_list_sin_comprimir[4251]))