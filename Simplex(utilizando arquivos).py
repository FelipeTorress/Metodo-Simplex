def encontrarCoeficientes(linha,listaDeCoeficientes):
    indexX = -1
    count = -1
    for palavra in linha:
            count+=1    
            indexX = -1
            for letra in palavra:
                indexX+=1
                if letra == 'X' or letra == 'x':
                    if count > 0:
                        if linha[count - 1] == '-':
                            listaDeCoeficientes.append(-1*float(palavra[:indexX]))
                        else:
                            listaDeCoeficientes.append(float(palavra[:indexX]))
                    else:
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
    with open('dados3.txt', 'r') as arquivo:
        objetivo = arquivo.readline()
        for linha in arquivo.readlines():
            quantLinhas+=1
            restricao.append(linha.split(' '))
    return objetivo, restricao, quantLinhas

def encontrarVariaveis(basicas, naobasica, quantDeLinhas, quantDeVariaveis): 
    num = quantDeVariaveis - 1 - quantDeLinhas 

    for i in range(num):
        naobasica.append('x'+str(i+1))

    num = num + 1
    for i in range(quantDeLinhas):
        basicas.append('x'+str(i+num))
    
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
        valor =tableau[i][indexVariavelParaEntrar]
        if valor > 0:
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
            aux = tableau[i][indexEntrar] * -1
            

            for j in range( len(tableau[0]) ):
                linha.append(tableau[indexSair][j] * aux + tableau[i][j])
              
            tableau[i] = linha    


        elif i != indexSair and tableau[i][indexEntrar] < 0: 
            linha = []
            aux = tableau[i][indexEntrar] * -1

            for j in range( len(tableau[0]) ):
                linha.append(tableau[indexSair][j] * aux + tableau[i][j])
              
            tableau[i] = linha
    
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
        
        if indexVariavelParaSair == -1: #sem solução
            return None

        tableau = trocarVariaveis(indexVariavelParaEntrar,indexVariavelParaSair, variaveisNaoBasicas, variaveisBasicas, tableau)
    return tableau
    
def resultados(tableau, vetorBasico, vetorNaoBasico, objetivo, restricao):

    if tableau == None:
        print('o Problema possui infinitas soluções')
    else:
        print('Problema Inicial: ')
        print(objetivo)
        frase = ''
        for i in range(len(restricao)):
            frase=''
            for j in restricao[i]:
                frase = frase+' '+j
            print(frase)


        tableauFinal =[]

        for linha in range(len(tableau)):
            aux = []
            for coluna in range(len(tableau[0])):
                aux.append(round(tableau[linha][coluna], 1))
            tableauFinal.append(aux)

        print('\tTableau Final:')

        for linha in range(len(tableau)):
            print('   '+str(tableauFinal[linha]))

        print('Variáveis Básicas: '+str(vetorBasico))
        print('Variáveis Não Básicas: '+str(vetorNaoBasico))
        print('Valor de Z = '+ str( tableauFinal[len(tableauFinal) - 1] [len(tableauFinal[0])-1 ] ) )

'''def acharBases(tableau):
    bases = []
    for c in range(len(tableau[0])-1):
        aux = 0
        aux2 = 0
        for l in range(len(tableau[:-1])):
            if not tableau[l][c]==0 and not tableau[l][c]==1:
                aux=-1
            elif tableau[l][c]==1 and not aux==-1:
                aux+=1
                aux2=c
        if aux==1:
            bases.append('x'+str(aux2+1))
    base=[]
    for l in range(len(tableau)):
        for n in range(len(tableau[0])):
            for b in range(len(bases)):
                if tableau[l][n]==1 and ('x'+str(n+1) in bases[b]):
                    base.append(bases[b])
    return base'''

def main():
    tableau = []
    basicas = []
    naobasicas = []

    funccObjetivo, restricao, quantLinhas = lerArquivo()
    objetivo = funccObjetivo 
    objetivo = isMaximizar(objetivo) # saber se é de maximizar ou minimizar(multiplicando por -1 se for minimizar)
    tableau = montarTableau(objetivo, restricao, quantLinhas)
    basicas, naobasicas = encontrarVariaveis(basicas,naobasicas, quantLinhas,len(tableau[0]))
    tableau = resolverTableau(tableau,basicas,naobasicas)
    resultados(tableau, basicas, naobasicas, funccObjetivo, restricao)

main()