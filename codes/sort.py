from includes.header import attrgetter

def sortArray(array, order):
    quicksort(array, 0, len(array)-1, order)

def quicksortFromKey(array, key, inicio, fim):
    getKeyArray = attrgetter(key)
    keyArray = list(map(getKeyArray, array))
    # Se as keys forem um array de string, remove a capitalização
    if type(keyArray[0]) is str:
        for i in range(len(keyArray)):
            keyArray[i] = keyArray[i].lower()

    l = [inicio, fim]

    while len(l) > 0:
      novo_inicio = l.pop(0) # Armazena o primeiro elemento da lista e o remove --> Limite esquerdo
      novo_fim = l.pop(0) # Armazena o segundo (agora primeiro) elemento da lista e o remove --> Limite direito
      if novo_inicio < novo_fim:
          pivo = particionaFromKey(array, keyArray, novo_inicio, novo_fim)
          l.extend([novo_inicio, pivo - 1, pivo + 1, novo_fim])
          # Esses 4 parâmetros são respectivamente: limites esquerdo e direito da subárvore esquerda, e limites esquerdo e direito da subárvore direita

def particionaFromKey(array, keyArray, esquerda, direita):
    ind_mediana = busca_mediana(keyArray, esquerda, direita) # Mediana entre os 3 elementos (inicio, meio e fim)
    
    if keyArray[ind_mediana] != keyArray[direita]:
        array[ind_mediana], array[direita] = array[direita], array[ind_mediana] # Swap do pivo com ultimo elemento para utilizar algoritmo de Cormen
        keyArray[ind_mediana], keyArray[direita] = keyArray[direita], keyArray[ind_mediana]

    # Algoritmo de Partição de Cormen   
    pivo = direita
    i = esquerda - 1
    j = esquerda

    while j <= (direita - 1):
        if keyArray[j] <= keyArray[pivo]:
            i += 1
            array[i], array[j] = array[j], array[i]
            keyArray[i], keyArray[j] = keyArray[j], keyArray[i]
        j += 1

    array[i+1], array[direita] = array[direita], array[i+1]
    keyArray[i+1], keyArray[direita] = keyArray[direita], keyArray[i+1]

    return (i + 1)

def quicksort(array, inicio, fim, order):
    # Se as keys forem um array de string, remove a capitalização
    if type(array[0]) is str:
        for i in range(len(array)):
            array[i] = array[i].lower()

    l = [inicio, fim]

    while len(l) > 0:
      novo_inicio = l.pop(0) # Armazena o primeiro elemento da lista e o remove --> Limite esquerdo
      novo_fim = l.pop(0) # Armazena o segundo (agora primeiro) elemento da lista e o remove --> Limite direito
      if novo_inicio < novo_fim:
          pivo = particiona(array, novo_inicio, novo_fim, order)
          l.extend([novo_inicio, pivo - 1, pivo + 1, novo_fim])
          # Esses 4 parâmetros são respectivamente: limites esquerdo e direito da subárvore esquerda, e limites esquerdo e direito da subárvore direita

def particiona(array, esquerda, direita, order):
    ind_mediana = busca_mediana(array, esquerda, direita) # Mediana entre os 3 elementos (inicio, meio e fim)

    if array[ind_mediana] != array[direita]:
        array[ind_mediana], array[direita] = array[direita], array[ind_mediana] # Swap do pivo com ultimo elemento para utilizar algoritmo de Cormen

    # Algoritmo de Partição de Cormen   
    pivo = direita
    i = esquerda - 1
    j = esquerda

    while j <= (direita - 1):
        if order == 'a':
            test = array[j] <= array[pivo]
        elif order == 'd':
            test = array[j] >= array[pivo]
        if test:
            i += 1
            array[i], array[j] = array[j], array[i]
        j += 1

    array[i+1], array[direita] = array[direita], array[i+1]

    return (i + 1)

def busca_mediana(array, esquerda, direita):
  meio = int((esquerda+direita)/2)
  indices = [esquerda, direita, meio]
  array_combinado_ordenado = sorted([array[esquerda],array[direita], array[meio]])
  for i in indices:
    if array[i] == array_combinado_ordenado[1]:
      return i