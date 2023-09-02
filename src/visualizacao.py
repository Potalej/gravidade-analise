"""
  Funcoes para a visualizacao dos dados.
"""
import matplotlib.pyplot as plt
import config
from auxiliares.shapedynamics import mudar_somente_posicao

def visualizar_3d (R:list):
  """
    Visualizacao 3d das posicoes.
  """
  fig = plt.figure(figsize=(7,7), dpi=100)
  ax = fig.add_subplot(projection='3d')

  for Ri in R:
    ax.scatter(*Ri[0])
    Ri = list(zip(*Ri))
    ax.plot(Ri[0], Ri[1], Ri[2])

  ax.set_xlim3d(*config.RANGE_PLOT_X)
  ax.set_ylim3d(*config.RANGE_PLOT_Y)
  ax.set_zlim3d(*config.RANGE_PLOT_Z)
  plt.show()

def visualizar_2d (R:list):
  """
    Visualizacao 2d das posicoes.
  """
  fig = plt.figure(figsize=(7,7), dpi=100)
  ax = fig.add_subplot()

  for Ri in R:
    ax.scatter(*Ri[0])
    Ri = list(zip(*Ri))
    ax.plot(Ri[0], Ri[1])

  ax.set_xlim(*config.RANGE_PLOT_X)
  ax.set_ylim(*config.RANGE_PLOT_Y)
  plt.show()

def visualizar_sd_2d (m:list, R:list):
  """
    Visualizacao na descricao objetiva da 
    Shape Dynamics em 2d

    Parametros
    ----------
    m : list
      Lista de massas
    R : list
      Lista de posicoes das particulas
  """
  fig = plt.figure(figsize=(7,7), dpi=100)
  ax = fig.add_subplot()

  R = list(zip(*R))
  print(len(R), len(R[0]))
  coords = [[] for corpo in range(len(m))]
  for Ri in R:
    novas_coords = Ri
    novas_coords = mudar_somente_posicao(m, novas_coords)
    for i, coord in enumerate(novas_coords):
      coords[i].append(coord)

  for coord in coords:
    ax.scatter(*coord[0])
    coord = list(zip(*coord))
    ax.plot(coord[0], coord[1])

  plt.show()

def visualizar_sd_3d (m:list, R:list):
  """
    Visualizacao na descricao objetiva da 
    Shape Dynamics em 3d

    Parametros
    ----------
    m : list
      Lista de massas
    R : list
      Lista de posicoes das particulas
  """
  fig = plt.figure(figsize=(7,7), dpi=100)
  ax = fig.add_subplot(projection='3d')

  R = list(zip(*R))
  print(len(R), len(R[0]))
  coords = [[] for corpo in range(len(m))]
  for Ri in R:
    novas_coords = Ri
    novas_coords = mudar_somente_posicao(m, novas_coords)
    for i, coord in enumerate(novas_coords):
      coords[i].append(coord)

  for coord in coords:
    ax.scatter(*coord[0])
    coord = list(zip(*coord))
    ax.plot(coord[0], coord[1], coord[2])

  plt.show()
