from operator import attrgetter

def sortArray(array, key):
    quicksort(array, key, 0, len(array)-1)

def quicksort(array, key, inicio, fim):
    l = [inicio, fim]

    while len(l) > 0:
      novo_inicio = l.pop(0) # Armazena o primeiro elemento da lista e o remove --> Limite esquerdo
      novo_fim = l.pop(0) # Armazena o segundo (agora primeiro) elemento da lista e o remove --> Limite direito
      if novo_inicio < novo_fim:
          pivo = particiona(array, key, novo_inicio, novo_fim)
          l.extend([novo_inicio, pivo - 1, pivo + 1, novo_fim])
          # Esses 4 parâmetros são respectivamente: limites esquerdo e direito da subárvore esquerda, e limites esquerdo e direito da subárvore direita


def particiona(array, key, esquerda, direita):
    getKeyArray = attrgetter(key)
    keyArray = list(map(getKeyArray, array))

    ind_mediana = busca_mediana(keyArray, esquerda, direita) # Mediana entre os 3 elementos (inicio, meio e fim)
    
    if keyArray[ind_mediana] != keyArray[direita]:
        array[ind_mediana], array[direita] = array[direita], array[ind_mediana] # Swap do pivo com ultimo elemento para utilizar algoritmo de Cormen
        keyArray = list(map(getKeyArray, array))

    # Algoritmo de Partição de Cormen   
    pivo = direita
    i = esquerda - 1
    j = esquerda

    while j <= (direita - 1):
        if keyArray[j] <= keyArray[pivo]:
            i += 1
            array[i], array[j] = array[j], array[i]
            keyArray = list(map(getKeyArray, array))
        j += 1

    array[i+1], array[direita] = array[direita], array[i+1]
    keyArray = list(map(getKeyArray, array))

    return (i + 1)

def busca_mediana(array, esquerda, direita):
  meio = int((esquerda+direita)/2)
  indices = [esquerda, direita, meio]
  array_combinado_ordenado = sorted([array[esquerda],array[direita], array[meio]])
  for i in indices:
    if array[i] == array_combinado_ordenado[1]:
      return i