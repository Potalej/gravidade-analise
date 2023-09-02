from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips, vfx
from glob import glob

def juntar_videos (subdiretorio, nome_final):
  # Diretorio
  dir = f'./pontos/{subdiretorio}/*'
  videos = glob(dir)

  # Salva a lista de videos
  videos_lista = []
  for video in videos:
    nome_video = video.split('/')[-1]
    videos_lista.append(f"./pontos/{subdiretorio}/{nome_video}/video_{nome_video}.mp4")
    
  videos_lista.sort()
  print('Qntd:',len(videos_lista))

  # concatena os videos
  clipes = [VideoFileClip(video) for video in videos_lista]
  final = concatenate_videoclips(clipes)
  # final = final.fx(vfx.speedx,4)
  final.write_videofile(f'./pontos/{nome_final}.mp4')