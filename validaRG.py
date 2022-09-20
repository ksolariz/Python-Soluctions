def ValRG(numero):
    tamanho = len(numero)
    vetor = []

    if tamanho>=1:
        vetor.append(int(numero[0]) * 2)

    if tamanho>=2:
        vetor.append(int(numero[1]) * 3)

    if tamanho>=3:
        vetor.append(int(numero[2]) * 4)

    if tamanho>=4:
        vetor.append(int(numero[3]) * 5)

    if tamanho>=5:
        vetor.append(int(numero[4]) * 6)

    if tamanho>=6:
        vetor.append(int(numero[5]) * 7)

    if tamanho>=7:
        vetor.append(int(numero[6]) * 8)

    if tamanho>=8:
        vetor.append(int(numero[7]) * 9)

    if tamanho>=9:
        vetor.append(int(numero[8]) * 100)

    total = 0

    if tamanho>=1:
        total += vetor[0]

    if tamanho>=2:
        total += vetor[1]

    if tamanho>=3:
        total += vetor[2]

    if tamanho>=4:
        total += vetor[3]

    if tamanho>=5:
        total += vetor[4]

    if tamanho>=6:
        total += vetor[5]

    if tamanho>=7:
        total += vetor[6]

    if tamanho>=8:
        total += vetor[7]

    if tamanho>=9:
        total += vetor[8]

    resto = total % 11
    if resto != 0:
        return False
    else:
        return True

        
    





