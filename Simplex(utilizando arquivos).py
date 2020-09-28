def resultados(tableau, vetorBasico, vetorNaoBasico, objetivo, restricao):
    print('\nProblema Inicial: ')
    print(objetivo)
    frase = ''
    for i in range(len(restricao)):
        frase=''
        for j in restricao[i]:
            frase = frase+' '+j
        print(frase)
    print('\n')
    
    if tableau == None:
        print('\nNao foi possivel encontrar solucao Otima!')
        print('O Problema possui infinitas solucoes')
    elif tableau[len(tableau)-1] [ len(tableau[0]) -1 ] == 0:
        print('\nO Problema nao possui solucao viavel')
    else:
        tableauFinal =[]
        vetorSolucao = []
        for linha in range(len(tableau)):
            aux = []
            for coluna in range(len(tableau[0])):
                aux.append(round(tableau[linha][coluna], 1))
                
                if coluna == len(tableau[0])-1:
                    vetorSolucao.append(round(tableau[linha][coluna], 1))
            tableauFinal.append(aux)
        print('------SOLUCAO:-------- ')
        print('Tableau Final:\n')

        for linha in range(len(tableau)):
            print('   '+str(tableauFinal[linha]))

        print('\nVariaveis Basicas: '+str(vetorBasico)+" = "+str(vetorSolucao[:-1]))
        print('Variaveis Nao Basicas: '+str(vetorNaoBasico)+ ' = '+' [ 0 ] ')
        print('Valor de Z = '+ str( tableauFinal[len(tableauFinal) - 1] [len(tableauFinal[0])-1 ] ) )

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

def trocarVariaveis(indexEntrar, indexSair, naoBasicas, basicas, tableau):
    aux = 'x'+str(indexEntrar+1)
    aux2 = basicas[indexSair]

    vetAux = []
    for i in basicas:
        if i == aux2:
            vetAux.append(aux)
        else:
            vetAux.append(i)
    basicas = vetAux

    vetAux = []
    for i in naoBasicas:
        if i == aux:
            vetAux.append(aux2)
        else:
            vetAux.append(i)
    naoBasicas = vetAux
    
    return pivoteamento(tableau,indexEntrar,indexSair),basicas,naoBasicas#   Pivotear[indexSair][indexEntrar]  

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

def solucaoOtima(tableau):
    for i in tableau[len(tableau)-1]:
        if i > 0:
            return False
    return True

def resolverTableau(tableau, variaveisBasicas, variaveisNaoBasicas):
    while not solucaoOtima(tableau):
        indexVariavelParaEntrar = encontarVariavelParaEntrar(tableau,variaveisNaoBasicas)
        indexVariavelParaSair = encontrarVariavelParaSair(tableau,variaveisBasicas,indexVariavelParaEntrar)

        if indexVariavelParaSair == -1: #sem solução
            return None , None, None

        tableau,variaveisBasicas,variaveisNaoBasicas = trocarVariaveis(indexVariavelParaEntrar,indexVariavelParaSair, variaveisNaoBasicas, variaveisBasicas, tableau)

    return tableau, variaveisBasicas,variaveisNaoBasicas

def coeficienteFuncaoObjetivo(vetor, lista, quantDeVariaveis):
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

def acharBaseInicial(tableau):
    bases = []
    naoBasicas = []
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
    
    for i in range(len(tableau[0])-1):
        if ('x'+str(i+1)) in base:
            continue 
        else:
            naoBasicas.append('x'+str(i+1))
    
    return base, naoBasicas

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
    tableau.append(coeficienteFuncaoObjetivo(vetorAuxiliar[3:], listaDeCoeficientes, len(tableau[0])))

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

def lerArquivo(arquivo):
    restricao = []
    quantLinhas = 0
    with open(arquivo, 'r') as arquivo:
        objetivo = arquivo.readline()
        for linha in arquivo.readlines():
            quantLinhas+=1
            restricao.append(linha.split(' '))
    return objetivo, restricao, quantLinhas

def main(arquivo):
    tableau = []
    basicas = []
    naobasicas = []

    funccObjetivo, restricao, quantLinhas = lerArquivo(arquivo)#pegar dados do arquivo
    objetivo = funccObjetivo #backup da funcao objetiva original
    objetivo = isMaximizar(objetivo) #saber se é de maximizar ou minimizar(multiplicando por -1 se for minimizar)
    tableau = montarTableau(objetivo, restricao, quantLinhas)#montar o tablau inicial
    basicas, naobasicas = acharBaseInicial(tableau)#encontrar variaveis basicas iniciais
    tableau, basicas,naobasicas = resolverTableau(tableau,basicas,naobasicas)#encontrar resposta do simplex
    resultados(tableau, basicas, naobasicas, funccObjetivo, restricao)#imprimir respostas

while True :
    print('\n\nEntre com um arquivo(como especificado no readme): ')
    arquivo = input()
    if arquivo == '':
        continue
    else:
        main(arquivo)