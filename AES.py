import binascii
import numpy as np
from collections import deque

matriz_estado = [None] * 4
key_schedule = [None] * 10
s_box = [None] * 16
round_constant = [None] * 10
hex2bin_map = {
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

def gerar_sbox():
    linha1=['0x63','0x7c','0x77','0x7b','0xf2','0x6b','0x6f','0xc5','0x30','0x01','0x67','0x2b','0xfe','0xd7','0xab','0x76']
    linha2=['0xca','0x82','0xc9','0x7d','0xfa','0x59','0x47','0xf0','0xad','0xd4','0xa2','0xaf','0x9c','0xa4','0x72','0xc0']
    linha3=['0xb7','0xfd','0x93','0x26','0x36','0x3f','0xf7','0xcc','0x34','0xa5','0xe5','0xf1','0x71','0xd8','0x31','0x15']
    linha4=['0x04','0xc7','0x23','0xc3','0x18','0x96','0x05','0x9a','0x07','0x12','0x80','0xe2','0xeb','0x27','0xb2','0x75']
    linha5=['0x09','0x83','0x2c','0x1a','0x1b','0x6e','0x5a','0xa0','0x52','0x3b','0xd6','0xb3','0x29','0xe3','0x2f','0x84']
    linha6=['0x53','0xd1','0x00','0xed','0x20','0xfc','0xb1','0x5b','0x6a','0xcb','0xbe','0x39','0x4a','0x4c','0x58','0xcf']
    linha7=['0xd0','0xef','0xaa','0xfb','0x43','0x4d','0x33','0x85','0x45','0xf9','0x02','0x7f','0x50','0x3c','0x9f','0xa8']
    linha8=['0x51','0xa3','0x40','0x8f','0x92','0x9d','0x38','0xf5','0xbc','0xb6','0xda','0x21','0x10','0xff','0xf3','0xd2']
    linha9=['0xcd','0x0c','0x13','0xec','0x5f','0x97','0x44','0x17','0xc4','0xa7','0x7e','0x3d','0x64','0x5d','0x19','0x73']
    linha10=['0x60','0x81','0x4f','0xdc','0x22','0x2a','0x90','0x88','0x46','0xee','0xb8','0x14','0xde','0x5e','0x0b','0xdb']
    linha11=['0xe0','0x32','0x3a','0x0a','0x49','0x06','0x24','0x5c','0xc2','0xd3','0xac','0x62','0x91','0x95','0xe4','0x79']
    linha12=['0xe7','0xc8','0x37','0x6d','0x8d','0xd5','0x4e','0xa9','0x6c','0x56','0xf4','0xea','0x65','0x7a','0xae','0x08']
    linha13=['0xba','0x78','0x25','0x2e','0x1c','0xa6','0xb4','0xc6','0xe8','0xdd','0x74','0x1f','0x4b','0xbd','0x8b','0x8a']
    linha14=['0x70','0x3e','0xb5','0x66','0x48','0x03','0xf6','0x0e','0x61','0x35','0x57','0xb9','0x86','0xc1','0x1d','0x9e']
    linha15=['0xe1','0xf8','0x98','0x11','0x69','0xd9','0x8e','0x94','0x9b','0x1e','0x87','0xe9','0xce','0x55','0x28','0xdf']
    linha16=['0x8c','0xa1','0x89','0x0d','0xbf','0xe6','0x42','0x68','0x41','0x99','0x2d','0x0f','0xb0','0x54','0xbb','0x16']
    s_box[0] = linha1
    s_box[1] = linha2
    s_box[2] = linha3
    s_box[3] = linha4
    s_box[4] = linha5
    s_box[5] = linha6
    s_box[6] = linha7
    s_box[7] = linha8
    s_box[8] = linha9
    s_box[9] = linha10
    s_box[10] = linha11
    s_box[11] = linha12
    s_box[12] = linha13
    s_box[13] = linha14
    s_box[14] = linha15
    s_box[15] = linha16

def gerar_roundConstant():
    round_constant[0] = '0x01'
    round_constant[1] = '0x02'
    round_constant[2] = '0x04'
    round_constant[3] = '0x08'
    round_constant[4] = '0x10'
    round_constant[5] = '0x20'
    round_constant[6] = '0x40'
    round_constant[7] = '0x80'
    round_constant[8] = '0x1b'
    round_constant[9] = '0x36'

def gerar_chave(chave):
    index = 0
    index_aux = 0
    matriz_aux = [None] * 4
    for x in chave:      
        # matriz_aux[index] = binascii.hexlify(x.encode())
        matriz_aux[index] = hex(ord(x))
        index = index+1
        if index == 4:
            matriz_estado[index_aux] = matriz_aux
            matriz_aux = [None] * 4
            index_aux = index_aux + 1
            index = 0
    print(matriz_estado)
    gerar_key_schedule()
    
def gerar_key_schedule():
    index = 0
    round_key_0 = [None] * 4
    word_one = [None] * 4
    word_two = [None] * 4
    word_three = [None] * 4
    word_four = [None] * 4
    complete_key = [None] * 4
    for i in range(4):
        key_aux = matriz_estado[i]
        word_one[index] = key_aux[0]
        word_two[index] = key_aux[1]
        word_three[index] = key_aux[2]
        word_four[index] = key_aux[3]
        index = index + 1
    round_key_0[0] = word_one
    round_key_0[1] = word_two
    round_key_0[2] = word_three
    round_key_0[3] = word_four
    key_schedule[0] = round_key_0
    # key_schedule.insert(0,word_one)
    # key_schedule.insert(1,word_two)
    # key_schedule.insert(2,word_three)
    # key_schedule.insert(3,word_four)
    gerar_primeira_round_key()

def gerar_primeira_round_key(): #TODO
    for roundkey in range(1,10):
        roundkey_aux = key_schedule[roundkey - 1]
        print("ROUNDKEYAUX")
        print(roundkey_aux)
        word_aux = roundkey_aux[len(roundkey_aux)-1]
        print("WORDAUX")
        print(word_aux)
        print("KEYSCEHDULE")
        print(key_schedule)
        word_sbox = [None] * 4
        d = deque(word_aux)
        d.rotate(-1)
        print(d)
        for i in range(4):
            valor_lin = d[i][2:3] 
            valor_col = d[i][3:4] 
            word_sbox[i] = getSbox(valor_lin, valor_col)
        print("Word Sbox")
        print(word_sbox)
        word_roundkey = getRoundKey(roundkey-1)
        print("Word Roundkey")
        print(word_roundkey)
        first_rk = xorList(word_sbox, word_roundkey)
        print("Old KeySchedule:")
        print(key_schedule)
        print(first_rk)
        key_schedule[roundkey] = gerar_restantes_round_key(first_rk, roundkey)
        print("First rk:")
        
        print("New KeySchedule:")
        print(key_schedule)

def gerar_restantes_round_key(first_rk, roundkey):
    new_word = [None] * 4
    new_word[0] = first_rk
    key_schedule_aux = key_schedule[roundkey-1]
    for i in range(1,4):
        print(i)
        print("KEYSCHEDULEAUX:")
        print(key_schedule_aux[i])
        print("NEWWORD")
        print(new_word[i-1])
        new_word[i] = xorList(key_schedule_aux[i], new_word[i-1])
    print("newwordcompleta")
    print(new_word)
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
        first_binary = "".join([hex2bin_map[first_hex],hex2bin_map[second_hex]])
        second_binary = "".join([hex2bin_map[first_hex_sl],hex2bin_map[second_hex_sl]])
        padding = hex(int(xor(first_binary,second_binary),2))[2:].zfill(2)
        padding = "0x" + padding
        xor_list[i] = padding
    return xor_list

def xor(bit1,bit2): #Retorna string de bits resultante do xor entre 2 string de bits
    xor = ""
    for x in range(8):
            if(bit1[x] != bit2[x]):
                xor = xor + "1"
            else:
                xor = xor + "0"
    return xor

def getRoundKey(rk):
    word_rk = ['0x00'] * 4
    word_rk[0] = round_constant[rk]
    return word_rk

def getSbox(valor_lin, valor_col):
    index_lin = 0
    index_col = 0
    if(valor_lin == 'a'):
        index_lin = 10
    elif(valor_lin == 'b'):
        index_lin = 11
    elif(valor_lin == 'c'):
        index_lin = 12
    elif(valor_lin == 'd'):
        index_lin = 13
    elif(valor_lin == 'e'):
        index_lin = 14
    elif(valor_lin == 'f'):
        index_lin = 15
    else:
        index_lin = valor_lin
    if(valor_col == 'a'):
        index_col = 10
    elif(valor_col == 'b'):
        index_col = 11
    elif(valor_col == 'c'):
        index_col = 12
    elif(valor_col == 'd'):
        index_col = 13
    elif(valor_col == 'e'):
        index_col = 14
    elif(valor_col == 'f'):
        index_col = 15
    else:
        index_col = valor_col
    index_lin_asint = int(index_lin)   
    index_col_asint = int(index_col) 

    return(s_box[index_lin_asint][index_col_asint])


def main():
    gerar_sbox()
    gerar_roundConstant()
    print(round_constant)
    gerar_chave("ABCDEFGHIJKLMNOP")
    print("ASDFKFO")
    print(key_schedule[0])
    print(key_schedule[1])
    print(key_schedule[2])
    print(key_schedule[3])
    print(key_schedule[4])
    print(key_schedule[5])
    print(key_schedule[6])
    print(key_schedule[7])
    print(key_schedule[8])
    print(key_schedule[9])


if __name__ == "__main__":
    main()