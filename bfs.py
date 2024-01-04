# Importar numpy para operações com arrays
import numpy as np
# Importar collections para operações com filas FIFO
import collections

# Definir uma classe para os nós
class No:
  def __init__(self, estado, pai, acao, custo):
    self.estado = estado # O estado do nó
    self.pai = pai # O nó pai
    self.acao = acao # A ação que levou a este nó
    self.custo = custo # O custo do caminho desde o estado inicial até este nó

# Definir uma classe para o problema do quebra-cabeça de 8 peças
class QuebraCabecaOito:
  def __init__(self, estado_inicial):
    self.estado_inicial = estado_inicial # O estado inicial do quebra-cabeça
    self.estado_objetivo = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) # O estado objetivo do quebra-cabeça
    self.acoes = self.acoes # A função que retorna as ações disponíveis para um estado

  # Definir uma função para retornar as ações disponíveis para um estado
  def acoes(self, estado):
    # Encontrar a posição do espaço em branco
    i, j = np.where(estado == 0)
    # Criar uma lista vazia para as ações
    acoes = []
    # Verificar as direções possíveis e acrescentá-las à lista
    if i > 0:
      acoes.append("CIMA")
    if i < 2:
      acoes.append("BAIXO")
    if j > 0:
      acoes.append("ESQUERDA")
    if j < 2:
      acoes.append("DIREITA")
    # Retornar a lista de ações
    return acoes

  # Definir uma função para aplicar uma ação a um estado e retornar o estado resultante
  def resultado(self, estado, acao):
    # Encontrar a posição do espaço em branco
    i, j = np.where(estado == 0)
    # Criar uma cópia do estado
    novo_estado = estado.copy()
    # Aplicar a ação e trocar as peças
    if acao == "CIMA" and i > 0:
      novo_estado[i, j], novo_estado[i-1, j] = novo_estado[i-1, j], novo_estado[i, j]
    elif acao == "BAIXO" and i < 2:
      novo_estado[i, j], novo_estado[i+1, j] = novo_estado[i+1, j], novo_estado[i, j]
    elif acao == "ESQUERDA" and j > 0:
      novo_estado[i, j], novo_estado[i, j-1] = novo_estado[i, j-1], novo_estado[i, j]
    elif acao == "DIREITA" and j < 2:
      novo_estado[i, j], novo_estado[i, j+1] = novo_estado[i, j+1], novo_estado[i, j]
    # Retornar o novo estado
    return novo_estado

  # Definir uma função para verificar se um estado é o estado objetivo
  def teste_objetivo(self, estado):
    # Comparar o estado com o estado objetivo
    return np.array_equal(estado, self.estado_objetivo)

  # Definir uma função para calcular o custo de um passo de uma ação
  def custo_passo(self, estado, acao):
    # Retornar 1 para qualquer ação
    return 1
# Definir uma função para o algoritmo de busca em largura
def busca_largura(problema):
  quant_nos = 1
  # Criar um nó com o estado inicial
  no = No(problema.estado_inicial, None, None, 0)
  # Verificar se o estado inicial é o estado objetivo
  if problema.teste_objetivo(no.estado):
    return no
  # Criar uma fila FIFO e enfileirar o nó
  fronteira = collections.deque()
  fronteira.append(no)
  # Criar um conjunto vazio para os estados explorados
  explorados = set()
  # Repetir até que a fila esteja vazia
  while fronteira:
    #print(" Count fronteira", len(fronteira))
    # Desenfileirar um nó da fila
    no = fronteira.popleft()
    # Adicionar o estado do nó ao conjunto explorado como uma tupla
    explorados.add(tuple(no.estado.flatten()))
    print("Current node: ", no.estado)
    print("Frontier items: ", [no.estado for no in fronteira])

    # Percorrer as ações disponíveis para o estado do nó
    for acao in problema.acoes(no.estado):
      # Obter o nó filho aplicando a ação
      filho = No(problema.resultado(no.estado, acao), no, acao, no.custo + problema.custo_passo(no.estado, acao))
      # Verificar se o estado filho já foi explorado ou está na fronteira como uma tupla
      if tuple(filho.estado.flatten()) not in explorados and filho not in fronteira:
        quant_nos += 1
        # Verificar se o estado filho é o estado objetivo
        if problema.teste_objetivo(filho.estado):
          print("Quantidade de nós criados : ", quant_nos)
          print(" Count explorados", len(explorados))
          return filho
        # Enfileirar o nó filho na fila
        fronteira.append(filho)
  # Retornar None se nenhuma solução for encontrada
  return None

# Definir uma função para imprimir o caminho da solução
def imprime_solucao(no):
  # Criar uma lista vazia para o caminho
  caminho = []
  # Repetir até que o nó seja None
  while no:
    # Acrescentar o nó ao caminho
    caminho.append(no)
    # Mover para o nó pai
    no = no.pai
  # Inverter o caminho
  caminho.reverse()
  # Imprimir o caminho
  for no in caminho:
    # Imprimir o estado do nó
    print(no.estado)
    # Imprimir a ação do nó
    print(no.acao)
    # Imprimir o custo do nó
    print(no.custo)
    # Imprimir um separador
    print("-" * 10)

# Definir o estado inicial do quebra-cabeça
estado_inicial = np.array([[2, 8, 3], [1, 6, 4], [7, 0, 5]])
import datetime
start_time = datetime.datetime.now ()
# Criar uma instância do problema
problema = QuebraCabecaOito(estado_inicial)

# Chamar a função de busca em largura
solucao = busca_largura(problema)
end_time = datetime.datetime.now ()
time_elapsed = end_time - start_time
print ("Time taken: ", round (time_elapsed.microseconds / 1000))

# Imprimir a solução
if solucao:
  imprime_solucao(solucao)
else:
  print("Nenhuma solução encontrada")
