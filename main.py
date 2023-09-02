from datetime import datetime
from src.ler import *
from src.animacao import *
from src.visualizacao import *
from src.estatisticas import *
from src.juntar_videos import juntar_videos
import os
import matplotlib.pyplot as plt

DIVISOR_GRANDE = 53*'='
DIVISOR_PEQUENO = 26*'='

print(f"{DIVISOR_GRANDE} \n Leitura de arquivos gerados pelo gravidade-fortran \n{DIVISOR_GRANDE}\n")

dir = input('= Arquivo: \n> ')

print()

parcial_completo = input('= Quer ler por partes (0) ou completo (1)?')

if int(parcial_completo) == 1:
  massas, posicoes, momentos = ler_csv(dir)

  G = float(input('= Gravidade:\n> '))

  print(f"\n\n{DIVISOR_PEQUENO}\n\t Informações\n{DIVISOR_PEQUENO}\n")

  print("Quantidade de corpos:", len(massas))
  print("Quantidade de passos:", len(posicoes[0]))

  print(f'\n\n{DIVISOR_PEQUENO}\n\tEstatísticas\n{DIVISOR_PEQUENO}')

  estatisticas(massas, posicoes, momentos, G)

  data = datetime.now()
  print(data, '\n\n')

  # visualizar_sd(massas, posicoes)

  while True:
    formato_visualizacao = int(input('= Deseja visualizar a simulação?\n1 - Trajetórias;\n2 - Evolução;\n3 - Salvar simulação (3D);\n4 - Salvar simulação (2D);\n0 - Sair\n> '))
    if formato_visualizacao == 1:
      visualizar_3d(posicoes)
    elif formato_visualizacao == 2:
      visualizar_tempo_real(posicoes)
    elif formato_visualizacao == 3:
      salvar_animacao(posicoes, dim=3)
    elif formato_visualizacao == 4:
      salvar_animacao(posicoes, dim=2)
    elif formato_visualizacao == 0:
      break
    print('\n\n')

else:
  tamanhoChunk = 5000
  pular = 10
  G = float(input('= Gravidade:\n> '))
  # captura o cabecalho
  massas, N = ler_csv_cabecalho(dir)

  salvar_animacoes = int(input('= Salvar animacoes? (0) Nao; (1) Sim:\n> '))
  animacoes_2d = 0
  if salvar_animacoes:
    animacoes_3d = int(input('Animacoes em 2d (0) ou em 3d (1)?\n> '))
    fator_escala = input('Qual o fator de escala? Deixe vazio para 1\n> ')
    # Gera nome para o chunk
    nome_chunk = f"chunks_{round(time())}"
    os.mkdir(f'pontos/{nome_chunk}')
    if fator_escala == "": fator_escala = 1
    else: fator_escala = float(fator_escala)

  exibir_estatisticas = int(input('= Estatisticas? (0) Nao; (1) Sim:\n> '))


  # le os chunks
  infos_gerais = 0
  chunk = 0
  for posicoes, momentos in ler_csv_chunks(dir, tamanhoChunk, N):
    chunk += 1
    print('chunk ', chunk)
    # gera a animacao se for o caso
    if (salvar_animacoes):
      if animacoes_3d:
        salvar_animacao(posicoes, 3, fator_escala, nome_chunk)
      else:
        salvar_animacao(posicoes, 2, fator_escala, nome_chunk)
      print('animacao salva')

    # calcula as estatisticas sem exibir
    if exibir_estatisticas:
      infos = estatisticas(massas, posicoes, momentos, G, False, pular)
      if infos_gerais == 0:
        infos_gerais = infos
      else:
        for chave in infos:
          infos_gerais[chave] += infos[chave]

  # junta os videos
  juntar_videos(nome_chunk, nome_chunk)
  
  
  if exibir_estatisticas:
    # agora exibe as informacoes
    # plota os 4 graficos
    fig, ax = plt.subplots(2, 4, figsize=(16,8))
    
    ax[0][0].plot(infos_gerais["H"], label="H")
    ax[0][0].set_ylabel("H")
    ax[0][0].legend()
    
    ax[1][0].plot(infos_gerais["Jx"], label="Jx")
    ax[1][0].plot(infos_gerais["Jy"], label="Jy")
    ax[1][0].plot(infos_gerais["Jz"], label="Jz")
    ax[1][0].legend()

    ax[0][1].plot(infos_gerais["Px"], label="Px")
    ax[0][1].plot(infos_gerais["Py"], label="Py")
    ax[0][1].plot(infos_gerais["Pz"], label="Pz")
    ax[0][1].legend()

    ax[1][1].plot(infos_gerais["Rcmx"], label="Rcmx")
    ax[1][1].plot(infos_gerais["Rcmy"], label="Rcmy")
    ax[1][1].plot(infos_gerais["Rcmz"], label="Rcmz")
    ax[1][1].legend()

    ax[0][2].plot(infos_gerais["D"], label="D")
    ax[0][2].set_ylabel("D")
    ax[0][2].legend()

    ax[1][2].plot(infos_gerais["Icm"], label="Icm")
    ax[1][2].set_ylabel("Icm")
    ax[1][2].legend()

    ax[0][3].plot(infos_gerais["C"], label="Complex.")
    ax[0][3].set_ylabel("C")
    ax[0][3].legend()
    
    plt.show()

    # plota um so com a complexidade
    plt.plot(infos_gerais["C"], label="Complex.")
    plt.legend()
    plt.show()  