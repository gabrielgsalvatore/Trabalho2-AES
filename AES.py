import binascii
import time
import threading
from collections import deque

progresso_atual = 0
progresso_teto = 0
key_schedule = [None] * 11
nome = ''
multiply_matrix = [['0x02','0x03','0x01','0x01'],
['0x01','0x02','0x03','0x01'],
['0x01','0x01','0x02','0x03'],
['0x03','0x01','0x01','0x02'],]
s_box = [
    ['0x63','0x7c','0x77','0x7b','0xf2','0x6b','0x6f','0xc5','0x30','0x01','0x67','0x2b','0xfe','0xd7','0xab','0x76'],
    ['0xca','0x82','0xc9','0x7d','0xfa','0x59','0x47','0xf0','0xad','0xd4','0xa2','0xaf','0x9c','0xa4','0x72','0xc0'],
    ['0xb7','0xfd','0x93','0x26','0x36','0x3f','0xf7','0xcc','0x34','0xa5','0xe5','0xf1','0x71','0xd8','0x31','0x15'],
    ['0x04','0xc7','0x23','0xc3','0x18','0x96','0x05','0x9a','0x07','0x12','0x80','0xe2','0xeb','0x27','0xb2','0x75'],
    ['0x09','0x83','0x2c','0x1a','0x1b','0x6e','0x5a','0xa0','0x52','0x3b','0xd6','0xb3','0x29','0xe3','0x2f','0x84'],
    ['0x53','0xd1','0x00','0xed','0x20','0xfc','0xb1','0x5b','0x6a','0xcb','0xbe','0x39','0x4a','0x4c','0x58','0xcf'],
    ['0xd0','0xef','0xaa','0xfb','0x43','0x4d','0x33','0x85','0x45','0xf9','0x02','0x7f','0x50','0x3c','0x9f','0xa8'],
    ['0x51','0xa3','0x40','0x8f','0x92','0x9d','0x38','0xf5','0xbc','0xb6','0xda','0x21','0x10','0xff','0xf3','0xd2'],
    ['0xcd','0x0c','0x13','0xec','0x5f','0x97','0x44','0x17','0xc4','0xa7','0x7e','0x3d','0x64','0x5d','0x19','0x73'],
    ['0x60','0x81','0x4f','0xdc','0x22','0x2a','0x90','0x88','0x46','0xee','0xb8','0x14','0xde','0x5e','0x0b','0xdb'],
    ['0xe0','0x32','0x3a','0x0a','0x49','0x06','0x24','0x5c','0xc2','0xd3','0xac','0x62','0x91','0x95','0xe4','0x79'],
    ['0xe7','0xc8','0x37','0x6d','0x8d','0xd5','0x4e','0xa9','0x6c','0x56','0xf4','0xea','0x65','0x7a','0xae','0x08'],
    ['0xba','0x78','0x25','0x2e','0x1c','0xa6','0xb4','0xc6','0xe8','0xdd','0x74','0x1f','0x4b','0xbd','0x8b','0x8a'],
    ['0x70','0x3e','0xb5','0x66','0x48','0x03','0xf6','0x0e','0x61','0x35','0x57','0xb9','0x86','0xc1','0x1d','0x9e'],
    ['0xe1','0xf8','0x98','0x11','0x69','0xd9','0x8e','0x94','0x9b','0x1e','0x87','0xe9','0xce','0x55','0x28','0xdf'],
    ['0x8c','0xa1','0x89','0x0d','0xbf','0xe6','0x42','0x68','0x41','0x99','0x2d','0x0f','0xb0','0x54','0xbb','0x16'],
]

l_table = [['0x00','0x00','0x19','0x01','0x32','0x02','0x1a','0xc6','0x4b','0xc7','0x1b','0x68','0x33','0xee','0xdf','0x03'],
   ['0x64','0x04','0xe0','0x0e','0x34','0x8d','0x81','0xef','0x4c','0x71','0x08','0xc8','0xf8','0x69','0x1c','0xc1'],
   ['0x7d','0xc2','0x1d','0xb5','0xf9','0xb9','0x27','0x6a','0x4d','0xe4','0xa6','0x72','0x9a','0xc9','0x09','0x78'],
   ['0x65','0x2f','0x8a','0x05','0x21','0x0f','0xe1','0x24','0x12','0xf0','0x82','0x45','0x35','0x93','0xda','0x8e'],
   ['0x96','0x8f','0xdb','0xbd','0x36','0xd0','0xce','0x94','0x13','0x5c','0xd2','0xf1','0x40','0x46','0x83','0x38'],
   ['0x66','0xdd','0xfd','0x30','0xbf','0x06','0x8b','0x62','0xb3','0x25','0xe2','0x98','0x22','0x88','0x91','0x10'],
   ['0x7e','0x6e','0x48','0xc3','0xa3','0xb6','0x1e','0x42','0x3a','0x6b','0x28','0x54','0xfa','0x85','0x3d','0xba'],
   ['0x2b','0x79','0x0a','0x15','0x9b','0x9f','0x5e','0xca','0x4e','0xd4','0xac','0xe5','0xf3','0x73','0xa7','0x57'],
   ['0xaf','0x58','0xa8','0x50','0xf4','0xea','0xd6','0x74','0x4f','0xae','0xe9','0xd5','0xe7','0xe6','0xad','0xe8'],
   ['0x2c','0xd7','0x75','0x7a','0xeb','0x16','0x0b','0xf5','0x59','0xcb','0x5f','0xb0','0x9c','0xa9','0x51','0xa0'],
    ['0x7f','0x0c','0xf6','0x6f','0x17','0xc4','0x49','0xec','0xd8','0x43','0x1f','0x2d','0xa4','0x76','0x7b','0xb7'],
    ['0xcc','0xbb','0x3e','0x5a','0xfb','0x60','0xb1','0x86','0x3b','0x52','0xa1','0x6c','0xaa','0x55','0x29','0x9d'],
    ['0x97','0xb2','0x87','0x90','0x61','0xbe','0xdc','0xfc','0xbc','0x95','0xcf','0xcd','0x37','0x3f','0x5b','0xd1'],
    ['0x53','0x39','0x84','0x3c','0x41','0xa2','0x6d','0x47','0x14','0x2a','0x9e','0x5d','0x56','0xf2','0xd3','0xab'],
    ['0x44','0x11','0x92','0xd9','0x23','0x20','0x2e','0x89','0xb4','0x7c','0xb8','0x26','0x77','0x99','0xe3','0xa5'],
    ['0x67','0x4a','0xed','0xde','0xc5','0x31','0xfe','0x18','0x0d','0x63','0x8c','0x80','0xc0','0xf7','0x70','0x07'],]

e_table =  [['0x01','0x03','0x05','0x0f','0x11','0x33','0x55','0xff','0x1a','0x2e','0x72','0x96','0xa1','0xf8','0x13','0x35'],
 ['0x5f','0xe1','0x38','0x48','0xd8','0x73','0x95','0xa4','0xf7','0x02','0x06','0x0a','0x1e','0x22','0x66','0xaa'],
 ['0xe5','0x34','0x5c','0xe4','0x37','0x59','0xeb','0x26','0x6a','0xbe','0xd9','0x70','0x90','0xab','0xe6','0x31'],
 ['0x53','0xf5','0x04','0x0c','0x14','0x3c','0x44','0xcc','0x4f','0xd1','0x68','0xb8','0xd3','0x6e','0xb2','0xcd'],
 ['0x4c','0xd4','0x67','0xa9','0xe0','0x3b','0x4d','0xd7','0x62','0xa6','0xf1','0x08','0x18','0x28','0x78','0x88'],
 ['0x83','0x9e','0xb9','0xd0','0x6b','0xbd','0xdc','0x7f','0x81','0x98','0xb3','0xce','0x49','0xdb','0x76','0x9a'],
 ['0xb5','0xc4','0x57','0xf9','0x10','0x30','0x50','0xf0','0x0b','0x1d','0x27','0x69','0xbb','0xd6','0x61','0xa3'],
 ['0xfe','0x19','0x2b','0x7d','0x87','0x92','0xad','0xec','0x2f','0x71','0x93','0xae','0xe9','0x20','0x60','0xa0'],
 ['0xfb','0x16','0x3a','0x4e','0xd2','0x6d','0xb7','0xc2','0x5d','0xe7','0x32','0x56','0xfa','0x15','0x3f','0x41'],
 ['0xc3','0x5e','0xe2','0x3d','0x47','0xc9','0x40','0xc0','0x5b','0xed','0x2c','0x74','0x9c','0xbf','0xda','0x75'],
 ['0x9f','0xba','0xd5','0x64','0xac','0xef','0x2a','0x7e','0x82','0x9d','0xbc','0xdf','0x7a','0x8e','0x89','0x80'],
 ['0x9b','0xb6','0xc1','0x58','0xe8','0x23','0x65','0xaf','0xea','0x25','0x6f','0xb1','0xc8','0x43','0xc5','0x54'],
 ['0xfc','0x1f','0x21','0x63','0xa5','0xf4','0x07','0x09','0x1b','0x2d','0x77','0x99','0xb0','0xcb','0x46','0xca'],
 ['0x45','0xcf','0x4a','0xde','0x79','0x8b','0x86','0x91','0xa8','0xe3','0x3e','0x42','0xc6','0x51','0xf3','0x0e'],
 ['0x12','0x36','0x5a','0xee','0x29','0x7b','0x8d','0x8c','0x8f','0x8a','0x85','0x94','0xa7','0xf2','0x0d','0x17'],
 ['0x39','0x4b','0xdd','0x7c','0x84','0x97','0xa2','0xfd','0x1c','0x24','0x6c','0xb4','0xc7','0x52','0xf6','0x01'],]
round_constant = ['0x01','0x02','0x04','0x08','0x10','0x20','0x40','0x80','0x1b','0x36']
hex2bin_map = { #Conversor hex pra bin
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",    
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "a":"1010",
   "b":"1011",
   "c":"1100",
   "d":"1101",
   "e":"1110",
   "f":"1111",
}

def popular_matriz_estado(texto_simples):
    index = 0
    index_aux = 0
    matriz_estado = [None] * 4
    matriz_aux = [None] * 4
    for x in texto_simples:
        matriz_aux[index] = "0x" + hex(int(x))[2:].zfill(2)
        index = index+1
        if index == 4:
            matriz_estado[index_aux] = matriz_aux
            matriz_aux = [None] * 4
            index_aux = index_aux + 1
            index = 0
    return matriz_estado

def gerar_chave(chave): #Geramos a matriz estado a partir da chave
    index = 0
    index_aux = 0
    matriz_estado = popular_matriz_estado(chave)
    gerar_key_schedule(matriz_estado)
    
def gerar_key_schedule(matriz_estado): #Geramos o key schedule
    round_key_0 = [None] * 4
    word_one = [None] * 4 
    word_two = [None] * 4
    word_three = [None] * 4
    word_four = [None] * 4
    for i in range(4):
        key_aux = matriz_estado[i]
        if i == 0:
            word_one = key_aux #pegar cada palavra da matriz_estado
        elif i == 1:    
            word_two = key_aux
        elif i == 2:
            word_three = key_aux
        elif i == 3:    
            word_four = key_aux
    round_key_0[0] = word_one #botar as palavras numa lista que vai ser a nossa round_key raiz
    round_key_0[1] = word_two
    round_key_0[2] = word_three
    round_key_0[3] = word_four
    key_schedule[0] = round_key_0 #botar essa roundkey raiz na keyschedule
    gerar_primeira_round_key()

def gerar_primeira_round_key(): 
    for roundkey in range(1,11): #iterar por todas as roundkeys 
        roundkey_aux = key_schedule[roundkey - 1] #Pega a roundkey anterior para os cálculos
        word_aux = roundkey_aux[len(roundkey_aux)-1] #Pega a última palavra da roundkey anterior para gerar as primeiras roundkeys
        d = deque(word_aux) #usando deque para rotacionar a palavra
        d.rotate(-1) #rotacionando a palavra para a esquerda
        word_sbox = get_word_sbox(d) #retorna a palavra comparada com a s-table
        word_roundkey = getRoundKey(roundkey-1) #busca a roundkey constant a partir da rodada
        first_rk = xorList(word_sbox, word_roundkey) #xor da round constant com a word da sbox
        final_first_rk = xorList(first_rk, roundkey_aux[0]) #xor do xor anterior com a primeira palavra da roundkey anterior
        key_schedule[roundkey] = gerar_restantes_round_key(final_first_rk, roundkey) #Gera o restante das palavras desta roundkey passando a rodada e a primeira palavra gerada

def get_word_sbox(word):
    word_sbox = [None] * 4
    for i in range(4): #para cada valor hexa da palavra achar a linha e coluna
        valor_lin = "0x0"+(word[i][2:3]) #retirando o 0x do hexa e pegando o primeiro valor
        valor_col = "0x0"+(word[i][3:4])  #retirando 0x do hexa e pegando o segundo valor
        word_sbox[i] = s_box[int(valor_lin,0)][int(valor_col,0)] #populando a word_sbox a partir dos valores hexa
    return word_sbox



def get_matrix_sbox(matriz):
    word_sbox = [None] * 4
    matrix_sbox = [None] * 4
    new_word_sbox = [None] * 4
    for i in range(4):
        word_sbox = matriz[i]
        for x in range(4):
            valor_lin = "0x0"+word_sbox[x][2:3] #retirando o 0x do hexa e pegando o primeiro valor
            valor_col = "0x0"+word_sbox[x][3:4]  #retirando 0x do hexa e pegando o segundo valor
            new_word_sbox[x] = s_box[int(valor_lin,0)][int(valor_col,0)]

        matrix_sbox[i] = new_word_sbox
        new_word_sbox = [None] * 4
    return matrix_sbox

def gerar_restantes_round_key(first_rk, roundkey):
    new_word = [None] * 4 #inicializa uma nova word
    new_word[0] = first_rk #define a primeira word como a gerada anteriormente
    key_schedule_aux = key_schedule[roundkey-1] #para referenciar os valores da roundkey anterior
    for i in range(1,4): #para cara word na roundkey
        new_word[i] = xorList(key_schedule_aux[i], new_word[i-1]) #faça um xor entre a palavra anterior dessa roundkey, com a palavra na mesma posição na roundkey anterior
    return new_word

def xorList(fl,sl): #Retorna uma Lista de Word derivada de duas outras Listas de Word
    xor_list = [None] * 4 #Inicializa nova Word
    first_binary = ""
    second_binary = ""
    for i in range(4):
        first_hex = fl[i][2:3] #Pega somente o primeiro valor hex (bits esquerda)
        first_hex_sl = sl[i][2:3] #Pega somente o primeiro valor hex (bits esquerda)
        second_hex = fl[i][3:4] #Pega somente o segundo valor hex (bits direita)
        second_hex_sl = sl[i][3:4] #Pega somente o segundo valor hex (bits direita)
        first_binary = "".join([hex2bin_map[first_hex],hex2bin_map[second_hex]]) #pega os valores binários dos valores hexa
        second_binary = "".join([hex2bin_map[first_hex_sl],hex2bin_map[second_hex_sl]])
        padding = hex(int(xor(first_binary,second_binary),2))[2:].zfill(2) #faz um xor entre os valores binários
        padding = "0x" + padding #adiciona 0x novamente
        xor_list[i] = padding #adiciona a nova word na lista
    return xor_list


def xorHex(fh,sh): #Retorna uma Lista de Word derivada de duas outras Listas de Word
    xor_value = ""
    first_binary = ""
    second_binary = ""
    first_hex = fh[2:3] #Pega somente o primeiro valor hex (bits esquerda)
    first_hex_sh = sh[2:3] #Pega somente o primeiro valor hex (bits esquerda)
    second_hex = fh[3:4] #Pega somente o segundo valor hex (bits direita)
    second_hex_sh = sh[3:4] #Pega somente o segundo valor hex (bits direita)
    first_binary = "".join([hex2bin_map[first_hex],hex2bin_map[second_hex]]) #pega os valores binários dos valores hexa
    second_binary = "".join([hex2bin_map[first_hex_sh],hex2bin_map[second_hex_sh]])
    padding = hex(int(xor(first_binary,second_binary),2))[2:].zfill(2) #faz um xor entre os valores binários
    padding = "0x" + padding #adiciona 0x novamente
    xor_value = padding #adiciona a nova word na lista
    return xor_value

def xor(bit1,bit2): #Retorna string de bits resultante do xor entre 2 string de bits
    xor = ""
    for x in range(8):
            if(bit1[x] != bit2[x]):
                xor = xor + "1" #caso diferente retorna 1
            else:
                xor = xor + "0" #caso igual retorna 0
    return xor

def getRoundKey(rk):
    word_rk = ['0x00'] * 4 #inicializa uma lista com 0x00 em todas posiçoes
    word_rk[0] = round_constant[rk] #popula o primeiro valor com o valor da round_constant respectivo
    return word_rk

def progresso():
    while(progresso_atual < progresso_teto):
        time.sleep(0.25)
        print("Progresso: ",str(round((progresso_atual / progresso_teto)*100))+"%",end='\r')
    print("Cifragem Completa!")


def gerar_padding(texto_simples):
    global progresso_teto
    global progresso_atual
    progresso_teto = round(len(texto_simples) / 16)
    progresso_atual = 0
    t = threading.Thread(target=progresso)
    t.start()
    if len(texto_simples) > 16:
        palavra = b''
        index = 0
        tamanho_total = 17
        while index < tamanho_total:
            if index == tamanho_total-1:
                cifrar_texto(palavra)
                palavra = b''
                tamanho_total = tamanho_total + 16
                progresso_atual = progresso_atual + 1
            if index < len(texto_simples):
                palavra = palavra + bytes([texto_simples[index]])
                index = index + 1
            elif index < tamanho_total:
                if (tamanho_total - 1) - index < 9:
                    padding = (tamanho_total - 1) - index
                    while ((tamanho_total - 1) - index) != 0:
                        palavra = palavra + bytes([padding])
                        index = index + 1
                    cifrar_texto(palavra)
                    progresso_atual = progresso_atual + 1
                    # t._stop()
                    return
                elif tamanho_total - index < 16:
                    padding = (tamanho_total - 9) - index
                    while ((tamanho_total - 9) - index) != 0:
                        palavra = palavra + str(padding)
                        index = index + 1
    else:
        cifrar_texto(texto_simples)
        progresso_atual = progresso_atual + 1
        # t._stop()

def cifrar_texto(texto_simples):
    matriz_estado_ts = None
    matriz_estado_ts = popular_matriz_estado(texto_simples) #cria uma matriz estado com o texto_simples
    matriz_estado_ts_xor = [None] * 4
    for i in range(4):
        matriz_estado_ts_xor[i] = xorList(matriz_estado_ts[i], key_schedule[0][i]) #faz xor dessa matriz com roundkey0
    matriz_rodada = matriz_estado_ts_xor #define que agora essa é a matriz que vamos usar
    matriz_cifragem = [None] * 10
    matriz_cifragem[0] = matriz_rodada
    palavra_cifrada = None
    for rodada in range(1,11): #para cada umas das 10 rodadas
        matriz_transposta = [None] * 4
        matriz_estado_ts_xor_sbox = None
        matriz_estado_ts_xor_sbox = get_matrix_sbox(matriz_cifragem[rodada-1]) #pega a matriz rodada do momento e pega todos os valores dela da sbox e joga nessa nossa nova matriz que vai ser a etapa subbyte
        matriz_transposta = transpose_list(matriz_estado_ts_xor_sbox)
        matriz_rot_1 = deque(matriz_transposta[1])
        matriz_rot_2 = deque(matriz_transposta[2])
        matriz_rot_3 = deque(matriz_transposta[3])
        matriz_rot_1.rotate(-1)
        matriz_rot_2.rotate(-2)
        matriz_rot_3.rotate(-3)
        matriz_transposta[1] = matriz_rot_1 
        matriz_transposta[2] = matriz_rot_2 
        matriz_transposta[3] = matriz_rot_3
        matriz_estado_ts_xor_sbox = transpose_list(matriz_transposta)
        if rodada != 10:
            matriz_estado_mixcolumn = gerar_mixcolumn(matriz_estado_ts_xor_sbox) #Esse método vai retornar a nossa matriz mixcolumn
        else:
            matriz_estado_mixcolumn = matriz_estado_ts_xor_sbox
        addroundkey = [None] * 4
        for i in range(4):
            addroundkey[i] = xorList(matriz_estado_mixcolumn[i], key_schedule[rodada][i])
        if rodada != 10:
            matriz_cifragem[rodada] = addroundkey
        else:
            palavra_cifrada = addroundkey
    arquivo_output = open(nome, "ab")
    for i in range(len(palavra_cifrada)):
        for x in range(len(palavra_cifrada[i])):
            valor = palavra_cifrada[i][x]
            palavra_cifrada_bytes = bytes([int(valor,16)])
            arquivo_output.write(palavra_cifrada_bytes)

def apresentar_matriz(matriz, texto="", transposta = False):
    if transposta:
        matriz = transpose_list(matriz)

    if texto != "":
        print(texto)

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j] + " " ,end="")
        print()
    print()

def transpose_list(list):
    new_list = [None] * 4
    for index in range(4):
         new_list[index] = [list[0][index], list[1][index], list[2][index], list[3][index]]

    return new_list

def gerar_mixcolumn(matriz):
    new_matrix = [None] * 4

    for i in range(4):
        this_word = matriz[i] #pega a word que vamos multiplicar
        word_final = [None] * 4
        for x in range(4):
            this_value = this_word
            this_multiplier = multiply_matrix[x] #pega a coluna da matriz de multiplicacao
            new_value_0 = multiply_galois(this_value[0] ,this_multiplier[0])
            new_value_1 = multiply_galois(this_value[1] ,this_multiplier[1])
            new_value_2 = multiply_galois(this_value[2] ,this_multiplier[2])
            new_value_3 = multiply_galois(this_value[3] ,this_multiplier[3])
            new_xor_0 = xorHex(new_value_0,new_value_1) #aqui vamo pega e efetuar os xor da formula
            new_xor_1 = xorHex(new_xor_0,new_value_2)
            new_xor_2 = xorHex(new_xor_1,new_value_3)
            word_final[x] = new_xor_2 #joga esse valor na nossa lista
        new_matrix[i] = word_final
    return new_matrix

def get_e_table(value):
    valor_lin = "0x0"+value[2:3]
    valor_col = "0x0"+value[3:4]
    return e_table[int(valor_lin,0)][int(valor_col,0)]
    
def multiply_galois(fv,sv):
    if fv == "0x00" or sv == "0x00":#se algum desses valores for 0 ou 1 entra nas excecoes
        return "0x00"
    elif fv == "0x01":
        return sv
    elif sv == "0x01":
        return fv
    valor_lin = "0x0"+fv[2:3]
    valor_col = "0x0"+fv[3:4]
    resultado_0 = l_table[int(valor_lin,0)][int(valor_col,0)] #pega na l-table o valor do primeiro valor fv
    valor_lin = "0x0"+sv[2:3]
    valor_col = "0x0"+sv[3:4]
    resultado_1 = l_table[int(valor_lin,0)][int(valor_col,0)] #pega na l-table o valor do segundo valor sv
    soma = int(resultado_0,0) + int(resultado_1,0) #se nao cai em nenhuma dessas excecoes ele soma os 2 valores, convertendo pra int e somando
    if(soma > 255):
        soma = soma - 255
    padding = hex(soma)[2:].zfill(2)
    padding = "0x" + padding 
    resultado = get_e_table(padding) #resultado da soma da e-table
    return resultado #retorna esse resultado
            

def main():
    global nome
    print("Digite um nome para o arquivo cifrado final eg: texto")
    nome = input()
    update_file = open(nome, "w").close()
    print("Digite a localização do arquivo a ser cifrado eg:","c:/users/usuario/texto")
    arquivo = open(input(), 'rb')
    print("Digite a chave a ser usada de 16bytes separando os valores hexa por , eg: 01,02: ", end='')
    entrada = input().split(',')
    entrada_bytes = b''.join(bytes([int(h,16)]) for h in entrada)
    gerar_chave(entrada_bytes)
    gerar_padding(arquivo.read())


if __name__ == "__main__":
    main()
