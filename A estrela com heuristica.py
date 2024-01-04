# Importe o numpy para operações de matriz
import numpy as np

# Defina uma classe para os nós
class Node:
  def __init__(self, estado, pai, acao, custo, heuristica):
    self.estado = estado  # O estado do nó
    self.pai = pai  # O nó pai
    self.acao = acao  # A ação que levou a este nó
    self.custo = custo  # O custo do caminho do estado inicial para este nó
    self.heuristica = heuristica  # O valor heurístico deste nó
    self.avaliacao = custo + heuristica  # A função de avaliação deste nó

# Defina uma classe para o problema do quebra-cabeça de 8 peças
class OitoQuebraCabeca:
  def __init__(self, estado_inicial):
    self.estado_inicial = estado_inicial  # O estado inicial do quebra-cabeça
    self.estado_objetivo = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])  # O estado objetivo do quebra-cabeça
    self.acoes = self.acoes  # A função que retorna as ações disponíveis para um estado
    
  # Defina uma função para retornar as ações disponíveis para um estado
  def acoes(self, estado):
    # Encontre a posição do espaço em branco
    i, j = np.where(estado == 0)
    # Crie uma lista vazia para as ações
    acoes = []
    # Verifique as direções possíveis e adicione-as à lista
    if i > 0:
      acoes.append("CIMA")
    if i < 2:
      acoes.append("BAIXO")
    if j > 0:
      acoes.append("ESQUERDA")
    if j < 2:
      acoes.append("DIREITA")
    # Retorne a lista de ações
    return acoes

  # Defina uma função para aplicar uma ação a um estado e retornar o estado resultante
  def resultado(self, estado, acao):
    # Encontre a posição do espaço em branco
    i, j = np.where(estado == 0)
    # Crie uma cópia do estado
    novo_estado = estado.copy()
    # Aplique a ação e troque as peças
    if acao == "CIMA" and i > 0:
      novo_estado[i, j], novo_estado[i-1, j] = novo_estado[i-1, j], novo_estado[i, j]
    elif acao == "BAIXO" and i < 2:
      novo_estado[i, j], novo_estado[i+1, j] = novo_estado[i+1, j], novo_estado[i, j]
    elif acao == "ESQUERDA" and j > 0:
      novo_estado[i, j], novo_estado[i, j-1] = novo_estado[i, j-1], novo_estado[i, j]
    elif acao == "DIREITA" and j < 2:
      novo_estado[i, j], novo_estado[i, j+1] = novo_estado[i, j+1], novo_estado[i, j]
    # Retorne o novo estado
    return novo_estado

  # Defina uma função para verificar se um estado é o estado objetivo
  def teste_objetivo(self, estado):
    # Compare o estado com o estado objetivo
    return np.array_equal(estado, self.estado_objetivo)

  # Defina uma função para calcular o custo da etapa de uma ação
  def custo_etapa(self, estado, acao):
    # Retorne 1 para qualquer ação
    return 1

  # Defina uma função para calcular o valor heurístico de um estado
  def heuristica(self, estado):
    # Inicialize o valor heurístico como zero
    heuristica = 0
    # Itere pelas peças do estado
    for i in range(3):
      for j in range(3):
        # Obtenha o valor da peça
        valor = estado[i, j]
        # Pule o espaço em branco
        if valor == 0:
          continue
        # Encontre a posição correta da peça no estado objetivo
        x, y = np.where(self.estado_objetivo == valor)
        # Adicione a distância de Manhattan da peça ao valor heurístico
        heuristica += abs(i - x) + abs(j - y)
    # Retorne o valor heurístico
    return heuristica

# Defina uma função para o algoritmo de busca A*
def a_estrela(problema):
  quant_no = 1
  # Crie um nó com o estado inicial
  no = Node(problema.estado_inicial, None, None, 0, problema.heuristica(problema.estado_inicial))
  # Verifique se o estado inicial é o estado objetivo
  if problema.teste_objetivo(no.estado):
    return no
  # Crie um dicionário que mapeia cada estado fronteiriço para uma tupla de seu nó e seu valor de função de avaliação
  fronteira = {}
  fronteira[tuple(no.estado.flatten())] = (no, no.avaliacao)
  # Crie um conjunto vazio para os estados explorados
  explorados = set()
  # Inicialize o limite f como infinito
  limite_f = float('inf')
  # Repita até que o dicionário esteja vazio
  while fronteira:
    # Encontre o estado com o menor valor de função de avaliação no dicionário
    estado = min(fronteira, key=lambda s: fronteira[s][1])
    # Obtenha o nó e o valor da função de avaliação do estado
    no, valor_f = fronteira[estado]
    # Remova o estado do dicionário
    fronteira.pop(estado)
    print("Current node: ", no.estado)
    
    print("Frontier items: ", [no for no in fronteira])
    # Verifique se o valor da função de avaliação do nó é maior que o limite f
    if valor_f > limite_f:
      # Pule o nó
      continue
    # Adicione o estado do nó ao conjunto explorado como uma tupla
    explorados.add(tuple(no.estado.flatten()))
    # Itere pelas ações disponíveis para o estado do nó
    for acao in problema.acoes(no.estado):
      # Obtenha o nó filho aplicando a ação
      filho = Node(problema.resultado(no.estado, acao), no, acao, no.custo + problema.custo_etapa(no.estado, acao), problema.heuristica(problema.resultado(no.estado, acao)))
      # Verifique se o estado filho já foi explorado ou está na fronteira como uma tupla
      if tuple(filho.estado.flatten()) not in explorados and tuple(filho.estado.flatten()) not in fronteira:
        quant_no += 1
        # Verifique se o estado filho é o estado objetivo
        if problema.teste_objetivo(filho.estado):
          print("Quantidade de nós percorridos:", quant_no)
          print(" Count explorados", len(explorados))
          return filho
        # Adicione o estado do nó filho e seu valor de função de avaliação ao dicionário
        fronteira[tuple(filho.estado.flatten())] = (filho, filho.avaliacao)
      # Se o estado filho estiver na fronteira, verifique se o nó filho tem um custo de caminho menor do que o nó existente
      elif tuple(filho.estado.flatten()) in fronteira and filho.custo < fronteira[tuple(filho.estado.flatten())][0].custo:
        # Substitua o nó existente pelo nó filho no dicionário
        quant_no += 1
        fronteira[tuple(filho.estado.flatten())] = (filho, filho.avaliacao)
    # Atualize o limite f para o menor valor de função de avaliação de qualquer nó no dicionário
    if fronteira:
      limite_f = min(fronteira.values(), key=lambda t: t[1])[1]
    
  # Retorne None se nenhuma solução for encontrada
  return None, 

# Defina uma função para imprimir o caminho da solução
def imprimir_solucao(no):
  # Crie uma lista vazia para o caminho
  caminho = []
  # Repita até que o nó seja None
  while no:
    # Adicione o nó ao caminho
    caminho.append(no)
    # Mova para o nó pai
    no = no.pai
  # Inverta o caminho
  caminho.reverse()
  # Imprima o caminho
  for no in caminho:
    # Imprima o estado do nó
    print(no.estado)
    # Imprima a ação do nó
    print(no.acao)
    # Imprima o custo do nó
    print(no.custo)
    # Imprima um separador
    print("-" * 10)

# Defina o estado inicial do quebra-cabeça
estado_inicial = np.array([[2, 3, 0], [1, 5, 6], [4, 7, 8]])
import datetime
start_time = datetime.datetime.now ()

# Crie uma instância do problema
problema = OitoQuebraCabeca(estado_inicial)

# Chame a função de busca A*
solucao = a_estrela(problema)
end_time = datetime.datetime.now ()
time_elapsed = end_time - start_time
print ("Time taken: ", round (time_elapsed.microseconds / 1000))
# Imprima a solução
if solucao:
  imprimir_solucao(solucao)
else:
  print("Nenhuma solução encontrada")
