import matplotlib.pyplot as plt
from auxiliares.hamiltoniano import H, EC
from auxiliares.auxiliares import centro_massas, momentoAngular, momento_inercia_cm
from auxiliares.shapedynamics import momento_dilatacao, complexidade
from tabulate import tabulate
from statistics import mean

def estatisticas (m:list, R:list, P:list, G:float, exibir:bool=True, pular:int=1):
  """
    Exibe as estatísticas
  """
  infos = {
    "Jx": [], # momento angular
    "Jy": [], # momento angular
    "Jz": [], # momento angular
    "H": [], # energia
    "Rcmx": [], # centro de massas
    "Rcmy": [], # centro de massas
    "Rcmz": [], # centro de massas
    "Px": [],  # momento linear total
    "Py": [], # momento linear total
    "Pz": [], # momento linear total
    "D" : [], # momento de dilatacao,
    "Icm": [], # momento de inercia
    "C": [], # complexidade
  }
  R = list(zip(*R))
  P = list(zip(*P))

  for t in range(0, len(R), pular):

    Rt, Pt = R[t], P[t]
    J = momentoAngular(Rt, Pt)
    infos["Jx"] += [J[0]]
    infos["Jy"] += [J[1]]
    infos["Jz"] += [J[2]]

    Ptotal = [sum(list(zip(*Pt))[0]), sum(list(zip(*Pt))[1]), sum(list(zip(*Pt))[2])]
    infos["Px"] += [Ptotal[0]]
    infos["Py"] += [Ptotal[1]]
    infos["Pz"] += [Ptotal[2]]

    Rcm = centro_massas(m, Rt)
    infos["Rcmx"] += [Rcm[0]]
    infos["Rcmy"] += [Rcm[1]]
    infos["Rcmz"] += [Rcm[2]]

    energia = H(Rt, Pt, m, G)
    infos["H"] += [energia]

    D = momento_dilatacao(Rt, Pt)
    infos["D"] += [D]

    Icm = momento_inercia_cm(m, Rt)
    infos["Icm"] += [Icm]

    C = complexidade(Icm, sum(m), -EC(Pt, m))
    infos["C"] += [C]
  
  if exibir:

    # agora calcula as estatísticas
    H_info =  ["H",  infos["H"][0],  min(infos["H"]),  max(infos["H"]),  mean(infos["H"])]
    
    Jx_info = ["Jx", infos["Jx"][0], min(infos["Jx"]), max(infos["Jx"]), mean(infos["Jx"])]
    Jy_info = ["Jy", infos["Jy"][0], min(infos["Jy"]), max(infos["Jy"]), mean(infos["Jy"])]
    Jz_info = ["Jz", infos["Jz"][0], min(infos["Jz"]), max(infos["Jz"]), mean(infos["Jz"])]

    Px_info = ["Px", infos["Px"][0], min(infos["Px"]), max(infos["Px"]), mean(infos["Px"])]
    Py_info = ["Py", infos["Py"][0], min(infos["Py"]), max(infos["Py"]), mean(infos["Py"])]
    Pz_info = ["Pz", infos["Pz"][0], min(infos["Pz"]), max(infos["Pz"]), mean(infos["Pz"])]

    Rcmx_info = ["Rcmx", infos["Rcmx"][0], min(infos["Rcmx"]), max(infos["Rcmx"]), mean(infos["Rcmx"])]
    Rcmy_info = ["Rcmx", infos["Rcmy"][0], min(infos["Rcmy"]), max(infos["Rcmy"]), mean(infos["Rcmy"])]
    Rcmz_info = ["Rcmx", infos["Rcmz"][0], min(infos["Rcmz"]), max(infos["Rcmz"]), mean(infos["Rcmz"])]

    tabela = [H_info, Jx_info, Jy_info, Jz_info, Px_info, Py_info, Pz_info, Rcmx_info, Rcmy_info, Rcmz_info]
    tabela = tabulate(tabela, headers=["Integral", "Inicial", "Min", "Max", "Média"])
    print()
    print(tabela, end="\n\n")

    fig, ax = plt.subplots(1, 4, figsize=(16,8))
    
    ax[0].plot(infos["H"], label="H")
    ax[0].set_ylabel("H")
    ax[0].legend()
    
    ax[1].plot(infos["Jx"], label="Jx")
    ax[1].plot(infos["Jy"], label="Jy")
    ax[1].plot(infos["Jz"], label="Jz")
    ax[1].legend()

    ax[2].plot(infos["Px"], label="Px")
    ax[2].plot(infos["Py"], label="Py")
    ax[2].plot(infos["Pz"], label="Pz")
    ax[2].legend()

    ax[3].plot(infos["Rcmx"], label="Rcmx")
    ax[3].plot(infos["Rcmy"], label="Rcmy")
    ax[3].plot(infos["Rcmz"], label="Rcmz")
    ax[3].legend()
    
    plt.show()
  
  return infos