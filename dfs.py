# Import numpy for array operations
import numpy as np

# Define a class for the nodes
class No:
  def __init__(self, estado, pai, acao, custo, profundidade):
    self.estado = estado # O estado do nó
    self.pai = pai # O nó pai
    self.acao = acao # A ação que levou a este nó
    self.custo = custo # O custo do caminho desde o estado inicial até este nó
    self.profundidade = profundidade # A profundidade do nó na árvore de busca

# Define a class for the 8 puzzle problem
class OitoPuzzle:
  def __init__(self, estado_inicial):
    self.estado_inicial = estado_inicial # O estado inicial do quebra-cabeça
    self.estado_final = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) # O estado final do quebra-cabeça
    self.acoes = self.acoes # A função que retorna as ações disponíveis para um estado

  # Define a function for returning the actions available for a state
  def acoes(self, estado):
    # Encontrar a posição do espaço em branco
    i, j = np.where(estado == 0)
    # Criar uma lista vazia para as ações
    acoes = []
    # Verificar as possíveis direções e acrescentá-las à lista
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

  # Define a function for applying an action to a state and returning the state resulting
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

  # Define a function for checking if a state is the goal state
  def teste_objetivo(self, estado):
    # Comparar o estado com o estado final
    return np.array_equal(estado, self.estado_final)

  # Define a function for calculating the step cost of an action
  def custo_passo(self, estado, acao):
    # Retornar 1 para qualquer ação
    return 1

# Define a function for the depth-first search algorithm
def busca_profundidade(problema, limite):
  quant_nos = 1
  no = No(problema.estado_inicial, None, None, 0, 0)
  if problema.teste_objetivo(no.estado):
    return no
  fronteira = [no]
  visitados = {}
  while fronteira:
    print("Current node: ", no.estado)
    print("Frontier items: ", [no.estado for no in fronteira])
    no = fronteira.pop()
    visitados[tuple(no.estado.flatten())] = no.profundidade
    for acao in problema.acoes(no.estado):
      filho = No(problema.resultado(no.estado, acao), no, acao, no.custo + problema.custo_passo(no.estado, acao), no.profundidade + 1)
      if filho.profundidade <= limite:
        if problema.teste_objetivo(filho.estado):
          print("Quantidade de nós finais criados : ", quant_nos)
          print(" Count explorados", len(visitados))
          return filho
        # Check if the state of the child node is already in the visited states or in the frontier
        if tuple(filho.estado.flatten()) not in visitados and not any(np.array_equal(filho.estado, node.estado) for node in fronteira):
          quant_nos += 1
          fronteira.append(filho)
  return None


# Define a function for printing the solution path
def imprimir_solucao(no):
  # Criar uma lista vazia para o caminho
  caminho = []
  # Repetir até o nó ser None
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
estado_inicial = np.array([[1, 3, 0], [4, 2, 5], [7, 8, 6]])
import datetime
start_time = datetime.datetime.now ()

# Criar uma instância do problema
problema = OitoPuzzle(estado_inicial)

# Chamar a função de busca em profundidade
solucao = busca_profundidade(problema,6)
end_time = datetime.datetime.now ()
time_elapsed = end_time - start_time
print ("Time taken: ", round (time_elapsed.microseconds / 1000))

# Imprimir a solução
if solucao:
  imprimir_solucao(solucao)
else:
  print("Nenhuma solução encontrada")
