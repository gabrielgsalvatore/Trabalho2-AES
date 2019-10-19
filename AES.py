import binascii

matriz_estado = [None] * 4


# def gerar_matriz():
#     matriz_estado = [None] * 4
#     for i in range(4):
#         x[i] = [None] * 4
#     return x

def gerar_chave(chave):
    index = 0
    index_aux = 0
    matriz_aux = [None] * 4
    for x in chave:
        print(index)
        
        matriz_aux[index] = binascii.hexlify(x.encode())
        index = index+1
        if index == 4:
            matriz_estado[index_aux] = matriz_aux
            matriz_aux = [None] * 4
            index_aux = index_aux + 1
            index = 0


def main():
    gerar_chave("ABCDEFGHIJKLMNOP")

    for x in matriz_estado:
        print(x)

if __name__ == "__main__":
    main()