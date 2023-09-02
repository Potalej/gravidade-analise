"""
  Script para leitura de arquivos integral ou parcialmente.
"""
from time import time
from pandas import read_csv
from config import DIRBASE 

def ler_csv (dir:str)->list:
  """
    Le um arquivo .CSV integralmente. 

    Parametros
    ----------
    dir : str 
      Diretorio do csv.

    Retorno
    -------
    massas : list
      Lista de massas dos corpos
    posicoes : list
      Lista de posicoes dos corpos
    momentos : list
      Lista de momentos lineares dos corpos.
  """

  tempo = time()
  print("Lendo o arquivo")

  # Captura o header
  massas, N = ler_csv_cabecalho(dir)
  
  # A quantidade de posicoes eh 6 * N
  qntdCols = 6*N

  # Agora le o resto
  df = read_csv(DIRBASE + dir, header=None, skiprows=[0], dtype=float)
  valores = df.values.tolist()

  # Converte o que foi lido em posicoes e momentos lineares
  posicoes, momentos = [[] for i in range(N)], [[] for i in range(N)]

  # Conversao dos dados
  print("Convertendo os dados...")
  for v in valores:
    for corpo in range(N):
      R = [v[corpo], v[corpo+N], v[corpo+2*N]]
      P = [v[3*N+corpo], v[3*N+corpo+N], v[3*N+corpo+2*N]]
      momentos[corpo].append(P)
      posicoes[corpo].append(R)
  
  tempo = round((time()-tempo)/10, 2)
  print(f"Dados capturados! ({tempo} ms)")

  return massas, posicoes, momentos

def ler_csv_cabecalho (dir:str)->list:
  """
    Le o cabecalho de um arquivo CSV, i.e., sua primeira linha,
    e retorna as massas e a quantidade de corpos.

    Parametros
    ----------
    dir : str 
      Diretorio do csv.

    Retorno
    -------
    massas : list
      Lista de massas dos corpos
    N : int
      Quantidade de corpos
  """
  # Captura o header para saber o tamanho
  df = read_csv(DIRBASE + dir, nrows=1, header=None)

  # Quantidade de corpos
  massas = df.values.tolist()[0]
  N = len(massas)
  return massas, N

def ler_csv_chunks (dir:str, tamanhoChunk:int, N:int):
  """
    Le um arquivo .CSV em chunks, sem armazena-lo totalmente
    na memoria.

    Parametros
    ----------
    dir : str 
      Diretorio do csv.
    tamanhoChunk : int
      Tamanho do chunk, i.e., quantida de linhas lidas.
    N : int
      Quantidade de corpos.
  """
  for df in read_csv(DIRBASE + dir, header=None, skiprows=[0], dtype=float, chunksize=tamanhoChunk):
    # Valores
    valores = df.values.tolist()
    # Converte o que foi lido em posicoes e momentos
    posicoes, momentos = [[] for i in range(N)], [[] for i in range(N)]
    # Converte os dados
    print("Convertendo os dados...")
    for v in valores:
      for corpo in range(N):
        R = [v[corpo], v[corpo+N], v[corpo+2*N]]
        P = [v[3*N+corpo], v[3*N+corpo+N], v[3*N+corpo+2*N]]
        posicoes[corpo].append(R)
        momentos[corpo].append(P)
    yield posicoes, momentos