"""
  Para gerar animacoes das simulacoes.
"""
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import config
from os import mkdir, remove, rmdir
from time import time
from moviepy.editor import *
from numpy import arange

def salvar_animacao (R:list, dim:int=3, fator_escala:float=1, nome_chunk:str=""):
  """
    Salva animacoes bidimensionais (eixos X e Y).
  """
  # Pula de 100 em 100
  posicoes = list(zip(*R))[::100]
  # Quantidade de subvideos
  qntd = 10

  # Nome da pasta
  pasta = str(round(time()))
  if nome_chunk == "": diretorio = f'pontos/{pasta}'
  else: diretorio = f'pontos/{nome_chunk}/{pasta}'

  # Cria o diretorio
  mkdir(diretorio)

  # Funcao para atualizar o frame
  atualizar = lambda t: atualizar_frame(ax, t, posicoes, dim=dim, fator_escala=fator_escala)

  # Gera os frames
  if int(len(posicoes)/qntd) == 0:
    # Se nao tiver ninguem, remove a pasta e encerra
    rmdir(diretorio)
    return

  for i in range(int(len(posicoes)/qntd)):
    print('Gerando frame ', i)
    funcao = lambda t: atualizar(qntd*i+t)
    fig = plt.figure(figsize=(7,7), dpi=config.ANIMACAO_DPI)
    # Gera os eixos
    if dim == 2: ax = fig.add_subplot()
    else: ax = fig.add_subplot(projection='3d')
    # Gera a nimacao
    ani = animation.FuncAnimation(fig, funcao, arange(qntd), interval=10, repeat=False)
    writervideo = animation.PillowWriter(fps=30)
    ani.save(f'{diretorio}/frame{i}.gif', writer=writervideo)
    plt.close()

  qntd_frames = int(len(posicoes)/qntd)

  del R
  del posicoes

  # Agora gera um arquivo de video
  frames = gerar_video(diretorio, pasta, qntd_frames)

  # Deleta os frames separados
  for arquivo in frames: remove(arquivo)

def gerar_video (diretorio:str, nome_pasta:str, qntd_frames:int):
  """
    Gera um video.
  """
  # Gerando arquivos de video
  arquivos = []
  frames = []
  dir = lambda i: f'{diretorio}/frame{i}.gif'
  for i in range(qntd_frames):
    frames.append(dir(i))
    clip = VideoFileClip(dir(i))
    arquivos.append(clip)
  # Concatena e salva
  final = concatenate_videoclips(arquivos)
  final.write_videofile(f'{diretorio}/video_{nome_pasta}.mp4')
  return frames

def atualizar_frame (ax, t, posicoes, dim, fator_escala):
  # Limpa e redefine
  ax.clear()
  # Limites de exibicao
  if dim == 2:
    ax.set_xlim(*config.RANGE_PLOT_X)
    ax.set_ylim(*config.RANGE_PLOT_Y)
  elif dim == 3:
    ax.set_xlim3d(*config.RANGE_PLOT_X)
    ax.set_ylim3d(*config.RANGE_PLOT_Y)
    ax.set_zlim3d(*config.RANGE_PLOT_Z)
  # Plota as particulas
  Rs = posicoes[t]
  Rs = list(zip(*Rs))
  X, Y, Z = Rs
  X = [x/fator_escala for x in X]
  Y = [y/fator_escala for y in Y]
  if dim == 3:
    Z = [z/fator_escala for z in Z]
  # Plota
  if dim == 2: ax.scatter(X, Y, c='black')
  elif dim == 3: ax.scatter(X, Y, Z, c='black')


def visualizar_tempo_real (R:list):

  posicoes = list(zip(*R))

  fig = plt.figure(figsize=(12,6), dpi=100)
  ax = fig.add_subplot(projection = '3d')

  def atualizar (t):
    ax.clear()
    ax.set_xlim3d(*config.RANGE_PLOT_X)
    ax.set_ylim3d(*config.RANGE_PLOT_Y)
    ax.set_zlim3d(*config.RANGE_PLOT_Z)
    # plota as partículas
    Rs = posicoes[t]
    for r in Rs:
      X, Y, Z = r
      ax.scatter(X, Y, Z, c="black")

  ax.set_xlim3d(*config.RANGE_PLOT_X)
  ax.set_ylim3d(*config.RANGE_PLOT_Y)
  ax.set_zlim3d(*config.RANGE_PLOT_Z)
  ani = animation.FuncAnimation(fig, atualizar, arange(len(posicoes)), interval=100, repeat=False)
  plt.show()