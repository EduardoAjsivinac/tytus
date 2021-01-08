# Seccion de Imports
import sys, os.path
import sys, os.path
gramaticaDir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(gramaticaDir)
from goto import with_goto
from gramatica import run_method


#Declaracion de variables
display = {}
p = 0
@with_goto
def procedurenuevo():
	global p
	t1= p - 1
	d = display[t1]
	t2= p - 1
	c = display[t2]
	t3= p - 1
	b = display[t3]
	t4= p - 1
	a = display[t4]
	p = p + 4
	t5 = 'Select * from usuarios;'
	display[p] = t5
	p = p + 1
	execute()
	if 5 > 6 :
		goto .L1
	goto .L2
	label .L1
	t6 = 1
	goto .L3
	label .L2
	t6 = 0
	label .L3
	if t6 == 1 :
		goto .L4
	goto .L5
	label .L4
	t7 = 'Select * from usuarios;'
	display[p] = t7
	p = p + 1
	execute()
	goto .L6
	label .L5
	t8 = 'Select * from usuarios;'
	display[p] = t8
	p = p + 1
	execute()
	label .L6


def execute():
	global p
	p=p-1
	resp = run_method(display[p])
	resp.execute(None)
	p=p+1


t3 = "USE HOLA;"
display[p] = t3
p = p + 1
t4 = "Select myfuncion('text');"
display[p] = t4
p = p + 1
