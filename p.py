
# Obtener resoluciones 

from pytube import YouTube
enlace = 'https://www.youtube.com/watch?v=GPf-e8sds20'
yt = YouTube(enlace)
resolution =[int(i.split("p")[0]) for i in (list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution])))]
resolution.sort()
resolution.reverse()
print(list(resolution))


from pytube import YouTube
import os
enlace = 'https://www.youtube.com/watch?v=GPf-e8sds20'
yt = YouTube(enlace)
audio = yt.streams.get_audio_only().download()
base, ext = os.path.splitext(audio)
new_file = base + '.mp3'
os.rename(audio, new_file)

import re
import requests
import urllib.request
link = "https://fb.watch/ecoR-mSPnv/"
html = requests.get(link)
try:
    url = re.search('hd_src:"(.+?)"',html.text)[1]
except:
    url = re.search('sd_src:"(.+?)"',html.text)[1]
print('Descargando video...')
urllib.request.urlretrieve(url,'video.mp4')
