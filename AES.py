import binascii
import numpy as np
from collections import deque

matriz_estado = [None] * 4
key_schedule = [None] * 10
s_box = [None] * 16

def gerar_sbox():
    linha1=["63","7c","77","7b","f2","6b","6f","c5","30","01","67","2b","fe","d7","ab","76"]
    linha2=["ca","82","c9","7d","fa","59","47","f0","ad","d4","a2","af","9c","a4","72","c0"]
    linha3=["b7","fd","93","26","36","3f","f7","cc","34","a5","e5","f1","71","d8","31","15"]
    linha4=["04","c7","23","c3","18","96","05","9a","07","12","80","e2","eb","27","b2","75"]
    linha5=["09","83","2c","1a","1b","6e","5a","a0","52","3b","d6","b3","29","e3","2f","84"]
    linha6=["53","d1","00","ed","20","fc","b1","5b","6a","cb","be","39","4a","4c","58","cf"]
    linha7=["d0","ef","aa","fb","43","4d","33","85","45","f9","02","7f","50","3c","9f","a8"]
    linha8=["51","a3","40","8f","92","9d","38","f5","bc","b6","da","21","10","ff","f3","d2"]
    linha9=["cd","0c","13","ec","5f","97","44","17","c4","a7","7e","3d","64","5d","19","73"]
    linha10=["60","81","4f","dc","22","2a","90","88","46","ee","b8","14","de","5e","0b","db"]
    linha11=["e0","32","3a","0a","49","06","24","5c","c2","d3","ac","62","91","95","e4","79"]
    linha12=["e7","c8","37","6d","8d","d5","4e","a9","6c","56","f4","ea","65","7a","ae","08"]
    linha13=["ba","78","25","2e","1c","a6","b4","c6","e8","dd","74","1f","4b","bd","8b","8a"]
    linha14=["70","3e","b5","66","48","03","f6","0e","61","35","57","b9","86","c1","1d","9e"]
    linha15=["e1","f8","98","11","69","d9","8e","94","9b","1e","87","e9","ce","55","28","df"]
    linha16=["8c","a1","89","0d","bf","e6","42","68","41","99","2d","0f","b0","54","bb","16"]
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

def gerar_chave(chave):
    index = 0
    index_aux = 0
    matriz_aux = [None] * 4
    for x in chave:      
        matriz_aux[index] = binascii.hexlify(x.encode())
        index = index+1
        if index == 4:
            matriz_estado[index_aux] = matriz_aux
            matriz_aux = [None] * 4
            index_aux = index_aux + 1
            index = 0
    gerar_key_schedule()
    
def gerar_key_schedule():
    index = 0
    word_one = [None] * 4
    word_two = [None] * 4
    word_three = [None] * 4
    word_four = [None] * 4
    for i in range(4):
        key_aux = matriz_estado[i]
        word_one[index] = key_aux[0]
        word_two[index] = key_aux[1]
        word_three[index] = key_aux[2]
        word_four[index] = key_aux[3]
        index = index + 1
    key_schedule.insert(0,word_one)
    key_schedule.insert(1,word_two)
    key_schedule.insert(2,word_three)
    key_schedule.insert(3,word_four)
    gerar_primeira_round_key()

def gerar_primeira_round_key(): #TODO
    word_aux = key_schedule[3]
    d = deque(word_aux)
    d.rotate(-1)
    for i in range(1):
        valor = binascii.unhexlify(d[i])
        index_lin = 0
        index_col = 0
        first = True
        for c in valor:
            print(valor)
            print(c)
            if(c == "a"):
                if(first):
                    index_lin = 10
                else:
                    index_col = 10
            elif(c == "b"):
                if(first):
                    index_lin = 11
                else:
                    index_col = 11
            elif(c == "c"):
                if(first):
                    index_lin = 12
                else:
                    index_col = 12
            elif(c == "d"):
                if(first):
                    index_lin = 13
                else:
                    index_col = 13
            elif(c == "e"):
                if(first):
                    index_lin = 14
                else:
                    index_col = 14
            elif(c == "f"):
                if(first):
                    index_lin = 15
                else:
                    index_col = 15
            else:
                if(first):
                    index_lin = c
                else:
                    index_col = c
            first = False
        print(index_col)
        print(index_lin)






    print(d)
    


def main():
    gerar_sbox()
    gerar_chave("ABCDEFGHIJKLMNOP")
    print(key_schedule)

    for x in matriz_estado:
        print(x)


if __name__ == "__main__":
    main()