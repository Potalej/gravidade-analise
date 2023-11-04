"""
  Faz a leitura por chunks
"""
from src.ler import *
from src.estatisticas import Estatisticas, saidaEstatisticas

def leitura_por_chunks (
  diretorio:str, 
  opcoes:dict,
  G:float=1, 
  tamanhoChunk:int=5000,
  qntdMaximaChunks:int=-1):

  # Le o cabecalho
  massas, N = ler_csv_cabecalho(diretorio)

  # Carrega por chunks
  chunk = 0
  for posicoes, momentos in ler_csv_chunks(diretorio, tamanhoChunk, N):
    chunk += 1
    if qntdMaximaChunks > 0 and chunk > qntdMaximaChunks: break

    # Faz os calculos
    # Classe de estatisticas
    ESTAT = Estatisticas(opcoes)
    saida = ESTAT.calculaMedidas(G, massas, posicoes, momentos)
    
  return saida