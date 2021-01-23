import pygame, sys
from pygame import *

"""
setSong: pasa las notas a minúsculas ya que la libreria recibe las notas en
minúsculas y como una tupla de tuplas, el 4 es la duración de la nota
"""
def setSong(notes):
	song=[]
	for x in notes:
		song.append((x.lower(), 4))
	song=tuple(song)
	return song

"""
reproducir: Guarda las notas como un .wav con los bpm indicados, después los reproduce con pygame
en caso del piano usa dos canales para reproducir cada una de las pistas (A veces no reproduce ambos wav :c ).
Crea una ventana de pygame para que el sonido se reproduzca, si no se crea el sonido no se reproduce.
pysynth_s imprime las frecuencias de las notas, pero lo hace desde el archivo pysynth.py, hay que modificarlo
"""	
def play(inst, songs, bPerM):
	pygame.mixer.init(48000, -16, 2, 1024)
	if inst==0:
		import pysynth_b 
		s0=setSong(songs[0])
		s1=setSong(songs[1])
		pysynth_b.make_wav(s0, fn="s0.wav", bpm=bPerM)
		pysynth_b.make_wav(s1, fn="s1.wav", bpm=bPerM)
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('s0.wav'))
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('s1.wav'))
		screen=pygame.display.set_mode((100, 100), 0, 32)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:                                                    
					pygame.quit()
					sys.exit()
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						pygame.quit()
						sys.exit()
		pygame.display.update()
	elif inst==1:
		import pysynth_s
		s0=setSong(songs[0])
		pysynth_s.make_wav(s0, fn="s0.wav", bpm=bPerM)
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('s0.wav'))
		screen=pygame.display.set_mode((100, 100), 0, 32)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:                                                    
					pygame.quit()
					sys.exit()
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						pygame.quit()
						sys.exit()
		pygame.display.update()
	elif inst==2:
		import pysynth_c
		s0=setSong(songs[0])
		pysynth_c.make_wav(s0, fn="s0.wav", bpm=bPerM)
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('s0.wav'))
		screen=pygame.display.set_mode((100, 100), 0, 32)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:                                                    
					pygame.quit()
					sys.exit()
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						pygame.quit()
						sys.exit()
		pygame.display.update()


#make_wav(test, fn="test.wav", bpm = 120)
#pysynth.make_wav(test, fn = "test.wav")
#print(test)
#test2=setSong(notes)
#print(setSong(notes))
#test=(('c', 4), ('e', 4), ('g', 4), ('c', 4))

"""
	Instrumentos
		0: piano
		1: guitarra
		2: bajo
	Songs
	Arreglo de arreglos, si es piano para tocar los dos arreglos de notas
	en otro caso sólo es una seríe de notas
"""

test=['A#3', 'B3', 'C3', 'C#3']
testA=[test]

play(2, testA, 120)

