from auxiliares.hamiltoniano import H, Ec, U
from auxiliares.auxiliares import momentoInerciaCm, momentoAngularTotal, centroDeMassas, momentoLinearTotal
from auxiliares.shapedynamics import momentoDilatacao, complexidade
from statistics import mean, median, stdev, variance
import matplotlib.pyplot as plt
from copy import copy
from math import ceil
from prettytable import PrettyTable

# EXEMPLO
# opcoesEstatisticas = {
#   # Valores que podem ser interessantes de ser obtidos
#   # Estar como True aqui significa que o valor sera salvo em uma lista e retornado
#   'energiaCinetica'    : False,
#   'energiaPotencial'   : False,
#   'energiaTotal'       : True,
#   'centroDeMassas'     : True,
#   'momentoLinearTotal' : True,
#   'momentoAngularTotal': True,
#   'momentoDeInercia'   : False,
#   'momentoDeDilatacao' : False,
#   'complexidade'       : False,
#   'taxaDeExpansao'     : False,

#   # Quantos passos pular entre cada estatistica
#   'qntdPassosPular': 1
# }

saidaEstatisticas = {
  # Lista de valores que forem calculados na classe de estatisticas
  'energiaCinetica'      : { 'nome': '$T$', 'valores': [], 'infos': dict() },
  'energiaPotencial'     : { 'nome': '$U$', 'valores': [], 'infos': dict() },
  'energiaTotal'         : { 'nome': '$E$', 'valores': [], 'infos': dict() },
  'centroDeMassas_X'     : { 'nome': '$R_{cmx}$', 'valores': [], 'infos': dict() },
  'centroDeMassas_Y'     : { 'nome': '$R_{cmy}$', 'valores': [], 'infos': dict() },
  'centroDeMassas_Z'     : { 'nome': '$R_{cmz}$', 'valores': [], 'infos': dict() },
  'momentoLinearTotal_X' : { 'nome': '$P_{x}$', 'valores': [], 'infos': dict() },
  'momentoLinearTotal_Y' : { 'nome': '$P_{y}$', 'valores': [], 'infos': dict() },
  'momentoLinearTotal_Z' : { 'nome': '$P_{z}$', 'valores': [], 'infos': dict() },
  'momentoAngularTotal_X': { 'nome': '$J_{x}$', 'valores': [], 'infos': dict() },
  'momentoAngularTotal_Y': { 'nome': '$J_{y}$', 'valores': [], 'infos': dict() },
  'momentoAngularTotal_Z': { 'nome': '$J_{z}$', 'valores': [], 'infos': dict() },
  'momentoDeInercia'     : { 'nome': '$I_{cm}$', 'valores': [], 'infos': dict() },
  'momentoDeDilatacao'   : { 'nome': '$D$', 'valores': [], 'infos': dict() },
  'complexidade'         : { 'nome': '$C_S$', 'valores': [], 'infos': dict() },
  'taxaDeExpansao'       : { 'nome': '$\mu$', 'valores': [], 'infos': dict() },
}

class Estatisticas:
  """
    Classe para o calculo das estatisticas.
  """
  def __init__ (self, opcoes:dict)->None:
    self.opcoes = opcoes

  def calculaMedidas (self, G:float, massas:list, posicoes:list, momentos:list):
    """
      Calcula as medidas desejadas sobre os dados.
    """
    # Cria a classe de saida
    saida = copy(saidaEstatisticas)
    
    # Separa as listas de posicoes e momentos
    R = list(zip(*posicoes))[::self.opcoes['qntdPassosPular']]
    P = list(zip(*momentos))[::self.opcoes['qntdPassosPular']]

    # Total de passos
    totalPassos = len(R)
    print('len de saida: ', len(saida['energiaTotal']['valores']))
    # Percorre os passos
    for t in range(0, totalPassos):
      # Captura as posicoes e os momentos lineares no instante t
      Rt, Pt = R[t], P[t]
      # Calculando os valores
      saida = self.calculaMedidas_passo(G, massas, Rt, Pt, saida)
    print('len de saida: ', len(saida['energiaTotal']['valores']))
    return saida

  def calculaMedidas_passo (self, G:float, massas:list, Rt:list, Pt:list, saida:dict)->dict:
    """
      Calcula os valores solicitados no parametro `opcoes`.
    """
    # Energia cinetica
    if self.opcoes['energiaCinetica']:
      EnCin = Ec(Pt, massas)
      saida['energiaCinetica']['valores'].append(EnCin)

    # Energia potencial
    if self.opcoes['energiaPotencial']:
      Ep = U(Rt, massas, G)
      saida['energiaPotencial']['valores'].append(Ep)

    # Energia total
    if self.opcoes['energiaTotal']:
      # Se ja tiver calculado energia cinetica, aproveita
      if self.opcoes['energiaCinetica']: EnCin = saida['energiaCinetica']['valores'][-1]
      else: 
        EnCin = Ec(Pt, massas)
      # Se ja tiver calculado a energia potencial, aproveita
      if self.opcoes['energiaPotencial']: Ep = saida['energiaPotencial']['valores'][-1]
      else: Ep = U(Rt, massas, G)
      # Salva a energia total
      Et = EnCin + Ep
      saida['energiaTotal']['valores'].append(Et)
    
    # Centro de massas
    if self.opcoes['centroDeMassas']:
      Rcm = centroDeMassas(massas, Rt)
      saida['centroDeMassas_X']['valores'].append(Rcm[0])
      saida['centroDeMassas_Y']['valores'].append(Rcm[1])
      saida['centroDeMassas_Z']['valores'].append(Rcm[2])

    # Momento linear total
    if self.opcoes['momentoLinearTotal']:
      Ptotal = momentoLinearTotal(Pt)
      saida['momentoLinearTotal_X']['valores'].append(Ptotal[0])
      saida['momentoLinearTotal_Y']['valores'].append(Ptotal[1])
      saida['momentoLinearTotal_Z']['valores'].append(Ptotal[2])

    # Momento angular total
    if self.opcoes['momentoAngularTotal']:
      Jtotal = momentoAngularTotal(Rt, Pt)
      saida['momentoAngularTotal_X']['valores'].append(Jtotal[0])
      saida['momentoAngularTotal_Y']['valores'].append(Jtotal[1])
      saida['momentoAngularTotal_Z']['valores'].append(Jtotal[2])

    # Momento de inercia
    if self.opcoes['momentoDeInercia']:
      Rcm = centroDeMassas(massas, Rt)
      Icm = momentoInerciaCm(massas, Rt, Rcm)
      saida['momentoDeInercia']['valores'].append(Icm)
    
    # Momento de dilatacao X
    if self.opcoes['momentoDeDilatacao']:
      Rcm = centroDeMassas(massas, Rt)
      D = momentoDilatacao(Rt, Pt, Rcm)
      saida['momentoDeDilatacao']['valores'].append(D)
    
    # Complexidade X
    if self.opcoes['complexidade']:
      # Se ja tiver calculado o momento de inercia, reutiliza
      if self.opcoes['momentoDeInercia']: Icm = saida['momentoDeInercia']['valores'][-1]
      else:
        Rcm = centroDeMassas(massas, Rt) 
        Icm = momentoInerciaCm(massas, Rt, Rcm)
      # Se ja tiver calculado a energia potencial, reutiliza
      if self.opcoes['energiaPotencial']: Ep = saida['energiaPotencial']['valores'][-1]
      else: Ep = U(Rt, massas, G)

      Cs = complexidade(Icm, sum(massas), Ep)
      saida['complexidade']['valores'].append(Cs)
    
    # Taxa de expansao X
    if self.opcoes['taxaDeExpansao']:
      # Se ja tiver calculado o momento de dilatacao, reutiliza
      if self.opcoes['momentoDeDilatacao']: D = saida['momentoDeDilatacao']['valores'][-1]
      else: 
        Rcm = centroDeMassas(massas, Rt) 
        D = momentoDilataca(Rt, Pt, Rcm)
      # Se ja tiver calculado o momento de inercia, reutiliza
      if self.opcoes['momentoDeInercia']: Icm = saida['momentoDeInercia']['valores'][-1]
      else: 
        Rcm = centroDeMassas(massas, Rt) 
        Icm = momentoInerciaCm(massas, Rt)
      
      taxaExp = D/Icm
      saida['taxaDeExpansao']['valores'].append(taxaExp)

    return saida

  def calculoEstatisticas (
    self,
    saidas_bruto  : dict,
    media         : bool = True,
    intervalo     : bool = True,
    desvio_padrao : bool = False,
    variancia     : bool = False,
    mediana       : bool = False
    )->dict:
    """
      Calcula as estatisticas das medidas calculadas a partir dos dados.

      Parametros
      ----------
      media : bool = True
        Calcula a media.
      intervalo : bool = True
        Calcula o minimo e o maximo dos dados.
      dp : bool = False
        Calcula o desvio padrao (dp).
      variancia : bool = False
        Calcula a variancia.
      mediana : bool = False
        Calcula a mediana.
    """
    saidas = dict()
    for medida in saidas_bruto:
      valores = saidas_bruto[medida]['valores']

      if len(valores)>0: saidas[medida] = saidas_bruto[medida]
      else: continue

      # Calcula as estatisticas
      if media:
        saidas[medida]['infos']['media'] = mean(valores)
      if intervalo:
        saidas[medida]['infos']['min'] = min(valores)
        saidas[medida]['infos']['max'] = max(valores)
      if desvio_padrao:
        saidas[medida]['infos']['dp'] = stdev(valores)
      if variancia:
        saidas[medida]['infos']['variancia'] = variance(valores)
      if mediana:
        saidas[medida]['infos']['mediana'] = median(valores)

    return saidas

  def tabelas (self, saida:dict)->None:
    """
    Exibe tabelas com os dados
    """
    tabela = PrettyTable()
    indice = 0
    # Percorre as medidas
    for medida in saida:
      if len(saida[medida]['valores']) > 0:
        dict_medida = saida[medida]
        estatisticas_medida = dict_medida['infos']
        if indice == 0:
          tabela.field_names = ['Medida'] + [*estatisticas_medida.keys()]
          indice+=1
        tabela.add_row(
          [dict_medida['nome']] + [*estatisticas_medida.values()]
        )
    print(tabela)
  
  def graficos (self, saida:dict, qntd_cols:int=4, min_comp:int=4, min_alt:int=4)->None:
    """
    Exibe graficos.
    """
    # Conta quantas opcoes estao habilitadas
    qntd_opcoes_habilitadas = 0
    for opcao in self.opcoes:
      if self.opcoes[opcao] and (opcao in saida or opcao + "_X" in saida):
        qntd_opcoes_habilitadas += 1
      
    # Calcula a quantidade de linhas e de colunas necessarias
    qntd_linhas = ceil(qntd_opcoes_habilitadas / qntd_cols)
    fig, axs = plt.subplots(qntd_linhas, qntd_cols, figsize=(qntd_cols*min_comp, qntd_linhas*min_alt))

    linha, coluna = 0, 0
    for opcao in self.opcoes:
      if self.opcoes[opcao]:
        # Agora verifica se eh uma opcao simples ou composta
        if opcao in saida:
          # Captura a opcao
          valOpc = saida[opcao]

          # Plota a evolucao do valor
          if qntd_linhas == 1:
            axs[coluna].plot(valOpc['valores'])
            axs[coluna].set_title(valOpc['nome'])
          else:
            axs[linha, coluna].plot(valOpc['valores'])
            axs[linha, coluna].set_title(valOpc['nome'])
        elif opcao + "_X" in saida:
          for eixo in ["X", "Y", "Z"]:
            # Captura a opcao
            valOpc = saida[opcao + "_" + eixo]
            nome = valOpc['nome'][:-3] + "}$"

            # Plota a evolucao do valor
            if qntd_linhas == 1:
              axs[coluna].plot(valOpc['valores'], label=valOpc['nome'])
              axs[coluna].set_title(nome)
              axs[coluna].legend()
            else:
              axs[linha, coluna].plot(valOpc['valores'], label=valOpc['nome'])
              axs[linha, coluna].set_title(nome)
              axs[linha, coluna].legend()
            
        # Atualiza valor da linha e da coluna
        coluna += 1
        if coluna == qntd_cols:
          coluna = 0
          linha += 1
    
    plt.show()
