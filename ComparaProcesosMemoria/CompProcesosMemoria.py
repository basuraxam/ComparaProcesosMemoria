#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom


def comparaProcesos(ap,apXML):
	dif = []
	for pXML in apXML:		
		i = 0		
		while ( (i < len(ap)) and (ap[i] != pXML) ):
			i += 1

		if ( i >= len(ap) ):
			dif.append(pXML)	
	
	for p in ap:		
		i = 0		
		while ( (i < len(apXML)) and (apXML[i] != p) ):
			i += 1

		if ( i >= len(apXML) ):
			dif.append(p)	
				
	return dif

#-----------------------------------------------------------------------	

def leerProcesosXML(fichero):
	procesosXML = []
	xmldoc = minidom.parse(fichero)
	itemlist = xmldoc.getElementsByTagName("Proceso")

	for i in itemlist:		
		procesosXML.append(i.attributes["Nombre"].value)

	return procesosXML
	
#-----------------------------------------------------------------------	

def leerProcesos():
	procesos = []
	for proc in psutil.process_iter():
		try:
			procesos.append(proc.name())
		except psutil.NoSuchProcess:
			pass
			
	return procesos

#-----------------------------------------------------------------------	
		
def grabarProcesosXML(fichero, procesosMem):
	if len(procesosMem) != 0:
		procesos = ET.Element('Procesos')
		for i in range(len(procesosMem)):
			proceso = ET.SubElement(procesos, 'Proceso')						 
			proceso.set('Nombre',procesosMem[i])
			
		mydata = ET.tostring(procesos)
		myfile = open(fichero, "w")
		myfile.write(mydata)
	else:
		print("No se han indicado procesos a grabar.")

#-----------------------------------------------------------------------	
	

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Comparador de procesos en memoria')

    parser.add_argument("-o","--opcion", help="c - comparar, g - grabar, m - mostrar", default = "m")
    parser.add_argument("-f","--file", help="Nombre del fichero a grabar o comparar", default = "ProcesosMemoria.xml")
    args = parser.parse_args()

    if args.opcion == 'c':
		#leemos los procesos
		pXML = leerProcesosXML(args.file)
		
		#Buscamos los procesos
		p = leerProcesos()
		
			
		dif = comparaProcesos(p, pXML)
		
		print("------- DIFERENCIA ----------------------")
		for d in dif:	
			print(d)
		print("-----------------------------------------")
    else:
		if args.opcion == 'g':
			
			procesosMem = leerProcesos()
			grabarProcesosXML(args.file,procesosMem)
			 
		else:
			if args.opcion == 'm':
				pMem= leerProcesos()
				for p in pMem:	
					print(p)
								
			else:
				print ('ERROR - Opción no valida.')

