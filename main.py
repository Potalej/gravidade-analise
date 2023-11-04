"""
  Quais analises eu tenho interesse em fazer?

  Valores interessantes:
  - Energia total (E);
  - Centro de massas (Rcm);
  - Momento linear total (P);
  - Momento angular total (J);
  - Energia cinética (Ec);
  - Energia potencial (U);
  - Momento de inercia (Icm);
  - Momento de dilatacao (D);
  - Complexidade (C);
  - Taxa de expansao (D/Icm).

  Acho que faz sentido deixar um checkbox com as coisas que quero calcular.

  VISUALIZACOES

  Posso pedir por tres tipos de visualizacao:
  - 2d (devo permitir a escolha de um eixo preferencial?);
  - 3d;
  - SD 2d;
  - SD 3d.

  E as visualizacoes podem ser geradas como trajetorias (linhas) ou salvando como animacoes.
"""
from src.ler import *
from src.estatisticas import Estatisticas
from src.chunks import leitura_por_chunks

#####################################
#              ENTRADA              #
#####################################

# Infos basicas
diretorio = "teste.csv"
G = 10

# Se desejar fazer a leitura parcial ou completa
leitura_parcial = True
tamanhoChunk = 100

# Opcoes das estatisticas
# Por padrao, estao ativados: E, Rcm, P, J
opcoesEstatisticas = {
  # Valores que podem ser interessantes de ser obtidos
  # Estar como True aqui significa que o valor sera salvo em uma lista e retornado
  'energiaCinetica'    : False,
  'energiaPotencial'   : False,
  'energiaTotal'       : True,
  'centroDeMassas'     : True,
  'momentoLinearTotal' : True,
  'momentoAngularTotal': True,
  'momentoDeInercia'   : False,
  'momentoDeDilatacao' : False,
  'complexidade'       : False,
  'taxaDeExpansao'     : False,

  # Quantos passos pular entre cada estatistica
  'qntdPassosPular': 1
}

#####################################
#              RODANDO              #
#####################################
estat = Estatisticas(opcoesEstatisticas)

if not leitura_parcial:
  # Le o arquivo
  massas, posicoes, momentos = ler_csv(diretorio)

  # Calcula os valores
  medidas = estat.calculaMedidas(G, massas, posicoes, momentos)
  print(len(medidas['energiaTotal']['valores']))

  # Calcula as estatisticas desejadas
  estatisticas_medidas = estat.calculoEstatisticas(
    medidas,
    media=True,
    intervalo=True
  )

  estat.tabelas(estatisticas_medidas)
  estat.graficos(medidas)


####################################
#        LEITURA POR CHUNKS        #
####################################
else:
  # Faz a leitura
  saidas_bruto = leitura_por_chunks(diretorio, opcoesEstatisticas, G, tamanhoChunk)
  
  # Calcula as estatisticas das medidas
  saidas = estat.calculoEstatisticas(saidas_bruto)

  # Cria a tabela
  estat.tabelas(saidas)
  
  # Cria os graficos
  estat.graficos(saidas)