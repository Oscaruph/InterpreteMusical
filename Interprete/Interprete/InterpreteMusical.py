"""
    Instituto Politecnico Nacional
    Escuela Superior de Computo 
    Unidad de Aprendiza:
        Compiladores
    Profesor:
        Rafael Norman Saucedo Delgado
    Alumno:
        Oscar Uriel Perez Hernandez
    Grupo:
        3CV6
    Proyecto:
        Interprete de Notas Musicales
    
"""
#Librerias Principales
import ply.lex as lex
import ply.yacc as yacc
import sys
import pygame
from pygame import *

#Tokens 
tokens = [

	'TIEMPO',
	'NOTA',
	'INS',
	'ID',
	'PAREA',
	'PAREC',
	'LLAVEA',
	'LLAVEC',
	'PIPE',
	'COMA',
	'PLAY',
]

#Tokens Basicos
t_PAREA = r'\('
t_PAREC = r'\)'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_PIPE = r'\|'
t_COMA = r'\,'
t_PLAY = r'[Pp][Ll][Aa][Yy]'

#Ignora espacios en blanco y tabulaciones
t_ignore_ESPACIOSBLANCOS = r"[ \t]+"

#Tokens Avanzados
 
#Expresion regular de notas musicales
def t_NOTA(t):
	r'(A[1-8]|A\#[1-8]|Bb[1-8]|B[1-8]|C[1-8]|C\#[1-8]|Db[1-8]|D[1-8]|D\#[1-8]|E[1-8]|F[1-8]|F\#[1-8]|Gb[1-8]|G[1-8])'
	t.type = 'NOTA'
	return t

#Instrumentos
def t_INS(t):
	r'(PIANO|GUITARRA|BAJO)'
	t.type = 'INS'
	return t

#Tiempos
def t_TIEMPO(t):
	r'\d+'
	t.value = int(t.value)
	return t

#ID´s
def t_ID(t):
	r'[\$][a-zA-z][a-zA-Z_0-9]*'
	t.type = 'ID'
	return t

#Saltos de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Errores
def t_error(t):
	print ("Error léxico en la línea %s  en  '%s'" % (t.lineno, t.value[0]))
	t.lexer.skip(1)

lexer = lex.lex()

# Gramatica

#Diccionario de funciones
global desFuncs

#playlist de notas
playFuncs = []

#Regla Principal
def p_InterpreteMusical(p):
	'''
	nuestroCompilador : expression
					  | empty
	'''
	print(p[1])

#Regla de funciones
def p_expression_function(p):
	'''
	expression : ID PAREA INS COMA TIEMPO PAREC LLAVEA notas LLAVEC
	'''
	if p[1] in desFuncs:
		print ("La función %s ya esta declarada" % p[1])
	elif p[5]<=128:
		desFuncs[p[1]] = [p[3],p[5],p[8]]
		p[0] = (p[1],p[3],p[5],p[8])
	else:
		print ("Tiempo %s excedido (128) en %s" % (p[5],p[1]))

#Regla de Expresiones Vacias
def p_expression_empty(p):
	'''
	expression : expression expression
	'''
	p[0] = (p[1],p[2])

#Regla Nota
def p_notas(p):
	'''
	notas : NOTA
	'''
	p[0] = p[1]

#Regla Multiples notas
def p_notas_many(p):
	'''
	notas : NOTA COMA notas
	'''
	p[0] = p[1]+','+p[3]

#Regla Reprodcuccion 
def p_expression_play(p):
	'''
	expression : PLAY PAREA r PAREC
	'''
	p[0] = (p[1],p[3])

#Regla para la reproduccion de una nota
def p_r(p):
	'''
	r : ID
	'''
	if p[1] in desFuncs:
		p[0] = p[1]
		playFuncs.append(p[1])
	else:
		print ("La función %s no esta declarada" % p[1])

#Regla para la reproduccion de varias notas
def p_r_many(p):
	'''
	r : ID COMA r
	'''
	if p[1] in desFuncs:
		p[0] = (p[1],p[3])
		playFuncs.append(p[1])
	else:
		print ("La función %s no esta declarada" % p[1])	

#Regla para la reproduccion de notas al mismo tiempo
def p_r_parallel(p):
	'''
	r : PAREA o PAREC
	'''
	p[0] = p[2]

#Regla para la reproduccion de una nota al mismo tiempo
def p_o(p):
	'''
	o : ID
	'''
	if p[1] in desFuncs:
		p[0] = p[1]
	else:
		print ("La función %s no esta declarada" % p[1])

#Regla para la reproduccion de varias notas al mismo tiempo
def p_o_many(p):
	'''
	o : ID PIPE o
	'''
	if p[1] in desFuncs:
		p[0] = (p[1],p[3])
	else:
		print ("La función %s no esta declarada" % p[1])
	
#Regla para linea vacia
def p_empty(p):
	'''
	empty :
	'''
	p[0] = None

def p_error(p):
    print ("Error sintáctico en la línea %s  en  '%s'" % (p.lineno, p.value))

funcs = {}
desFuncs = {}
parser = yacc.yacc()

#Manejo del archivo de entrada
file = open("Notas.fej", "r")
s = file.read()

#Analisis del archivo
parser.parse(s)

#Reproduccion 

def setSong(notes):
	song=[]
	for x in notes:
		song.append((x.lower(), 4))
	song=tuple(song)
	return song

"""
Reproduccion a traves de Pygame
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




"""
	Instrumentos
		0: piano
		1: guitarra
		2: bajo
"""

#Reproduccion de las notas musicales
print ("Diccionario de funciones")
print (desFuncs);
playFuncs.reverse()
print ("Lista de reproduccion")
print (playFuncs)
temp = []
for x in playFuncs:
	print ("Reproducir")
	print ("Nombre: %s" % x)
	print (desFuncs.get(x))
	temp = desFuncs.get(x)
	notas = temp.pop()
	tiempo = temp.pop()
	ins = temp.pop()
	numIns = -1
	if(ins=='PIANO'):
		numIns = 0
	elif(ins=='GUITARRA'):
		numIns = 1
	else:
		numIns = 2
	print ("Intrumento: %s - %d" % (ins, numIns))
	print ("Tiempo: %d" % tiempo)
	print ("Notas:")
	print (notas.split(","))
	play(numIns,notas.split(","),tiempo)