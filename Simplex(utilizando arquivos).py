def encontrarCoeficientes(linha,listaDeCoeficientes):
    indexX = -1
    for palavra in linha:

            indexX = -1
            for letra in palavra:
                indexX+=1
                if letra == 'X' or letra == 'x': 
                    listaDeCoeficientes.append(float(palavra[:indexX]))
                    break
    listaDeCoeficientes.append(float(linha[len(linha)-1]))

    return listaDeCoeficientes

def coeficienteFuncaoObjetiva(vetor, lista, quantDeVariaveis):
    variaveisBasicas = 0
    indexX = -1
    indexPalavra = -1

    for palavra in vetor:
            indexPalavra+=1
            indexX = -1
            for letra in palavra:
                indexX+=1
                if letra == 'X' or letra == 'x':
                    variaveisBasicas+=1
                    if vetor[indexPalavra-1] == '-':
                        lista.append(float(palavra[:indexX])* -1)
                    else:
                        lista.append(float(palavra[:indexX]))
                    break
    if quantDeVariaveis != variaveisBasicas:
        for i in range(quantDeVariaveis - variaveisBasicas):
            lista.append(float(0))

    return lista

def montarTableau(objetivo, restricao, quantLinhas):
    tableau = []
    listaDeCoeficientes = []

    #colocando as restriçoes
    for linha in restricao:
        listaDeCoeficientes = [] 
        tableau.append(encontrarCoeficientes(linha, listaDeCoeficientes))

    #colocando função objetiva
    listaDeCoeficientes = []
    vetorAuxiliar = objetivo.split()
    tableau.append(coeficienteFuncaoObjetiva(vetorAuxiliar[3:], listaDeCoeficientes, len(tableau[0])))

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
    with open('dados1.txt', 'r') as arquivo:
        objetivo = arquivo.readline()
        for linha in arquivo.readlines():
            quantLinhas+=1
            restricao.append(linha.split(' '))
    return objetivo, restricao, quantLinhas

def econtrarVariaveis(basicas, naobasica, quantDeLinhas, quantDeVariaveis):
    for i in range(quantDeVariaveis):
        if i == 0:
            continue
        elif i < quantDeLinhas:
            naobasica.append('x'+str(i))
        else:
            basicas.append('x'+str(i))
    return basicas, naobasica

def solucaoOtima(tableau):
    for i in tableau[len(tableau)-1]:
        if i > 0:
            return False
    return True

def encontarVariavelParaEntrar(tableau,variaveisNaoBasicas):
    maiornumero = 0
    indice = -1
    indiceParaEntrar = 0 

    linha = tableau[len(tableau)-1]
    for i in linha[:-1]:
        indice+=1
        if i >= maiornumero or indice == 0:
            maiornumero = i
            indiceParaEntrar = indice
    
    return indiceParaEntrar
        
def encontrarVariavelParaSair(tableau, variaveisBasicas, indexVariavelParaEntrar):
    menorValor = -1 
    indexParaSair = -1

    for i in range(len(tableau) - 1):
        if tableau[i][indexVariavelParaEntrar] > 0:
            valorAtual = tableau[i][len(tableau[i])-1] / tableau[i][indexVariavelParaEntrar]
            if menorValor > valorAtual or menorValor == -1:
                indexParaSair = i
                menorValor = valorAtual
    return indexParaSair

def pivoteamento(tableau, indexEntrar, indexSair):
    linha = []
    if tableau[indexSair][indexEntrar] != 1:
        for i in tableau[indexSair]:
            linha.append(i/tableau[indexSair][indexEntrar])
        
        tableau[indexSair] = linha

    
    for i in range(len(tableau)):
        if i != indexSair and tableau[i][indexEntrar] > 0:
            linha = []
            count = 0
            aux = tableau[i][indexEntrar] * -1
            

            for j in range( len(tableau[0]) ):
                linha.append(tableau[indexSair][j] * aux + tableau[i][j])
              
            tableau[i] = linha    


        elif i != indexSair and tableau[i][indexEntrar] < 0: 
                pass

            
    return tableau


def trocarVariaveis(indexEntrar, indexSair, naoBasicas, basicas,tableau):
    aux = naoBasicas[indexEntrar]
    aux2 = basicas[indexSair]

    naoBasicas[indexEntrar] = aux2
    basicas[indexSair] = aux
    
    return pivoteamento(tableau,indexEntrar,indexSair)#   Pivotear[indexSair][indexEntrar]  
    
def resolverTableau(tableau, variaveisBasicas, variaveisNaoBasicas):
    
    while not solucaoOtima(tableau):
        indexVariavelParaEntrar = encontarVariavelParaEntrar(tableau,variaveisNaoBasicas)
        indexVariavelParaSair = encontrarVariavelParaSair(tableau,variaveisBasicas,indexVariavelParaEntrar)
        print("entrar:"+ str(indexVariavelParaEntrar) +" sair:"+str(indexVariavelParaSair))
        tableau = trocarVariaveis(indexVariavelParaEntrar,indexVariavelParaSair, variaveisNaoBasicas, variaveisBasicas, tableau)
        print(tableau)

    return tableau

def main():
    objetivo, restricao, quantLinhas = lerArquivo()
    objetivo = isMaximizar(objetivo) # saber se é de maximizar ou minimizar(multiplicando por -1 se for minimizar)
    tableau = []
    tableau = montarTableau(objetivo, restricao, quantLinhas)
    variaveisBasicas = []
    variaveisNaoBasicas = []
    basicas, naobasicas = econtrarVariaveis(variaveisBasicas,variaveisNaoBasicas, quantLinhas,len(tableau[0]))
    print(tableau)
    print(basicas)
    print(naobasicas)
    tableau = resolverTableau(tableau,variaveisBasicas,variaveisNaoBasicas)
    print(tableau)
    print(basicas)
    print(naobasicas)


main()
