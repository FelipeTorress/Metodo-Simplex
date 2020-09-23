def montarTableau(objetivo, restricao, quantLinhas):
    tableau = []
    indexX = -1

    listaDeCoeficientes = []

    for linha in restricao:
        listaDeCoeficientes = []
    
        for palavra in linha:

            indexX = -1
            for letra in palavra:
                indexX+=1
                if letra == 'X' or letra == 'x': 
                    listaDeCoeficientes.append(int(palavra[:indexX]))
                    break
        tableau.append(listaDeCoeficientes)
    return tableau

   

def isMaximizar(objetivo):
    if "Max" in objetivo or "max" in objetivo:
        return objetivo
    elif "Min" in objetivo or "min" in objetivo:
        newString = "Max Z = "
        index = -1
        for i in objetivo.split():
            index+=1
            if "x" in i or "X" in i:
                if '-' in i and "+" in objetivo.split()[index-1]:
                    newString = newString+"+ "+i.replace('-','')+" "
                elif not "-" in i and  not "-" in objetivo.split()[index-1]:
                    newString = newString+"- "+i+" "
                elif "-" in i:
                    newString = newString+i.replace("-","")+" "
                else:
                    if(index != 4):
                        newString = newString+"+ "+i+" "
                    else:
                        newString = newString+" "+i+" "

        return newString


def lerArquivo():
    restricao = []
    quantLinhas = 0
    with open('dados.txt', 'r') as arquivo:
        objetivo = arquivo.readline()
        for linha in arquivo.readlines():
            quantLinhas+=1
            restricao.append(linha.split(' '))
    return objetivo, restricao, quantLinhas



objetivo, restricao, quantLinhas = lerArquivo()
print(objetivo)
print(restricao)
objetivo = isMaximizar(objetivo) # saber se é de maximizar ou minimizar(multiplicando por -1 se for minimizar)
print(objetivo)
tableau = []
tableau = montarTableau(objetivo, restricao, quantLinhas)
print(tableau)
