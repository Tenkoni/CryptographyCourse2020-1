#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fileinput

###s-boxes
s_zero = ((1,0,3,2),(3,2,1,0),(0,2,1,3),(3,1,3,2))
s_one = ((0,1,2,3),(2,0,1,3),(3,0,1,0),(2,1,0,3))

def chartobyte(char): #convierte caracteres o enteros a formato 8bit
	try:
		return(list(format(char, '08b')))
	except:
		return(list(format(ord(char), '08b')))

def initialper(inbyte): #permutacion inicial
	return([inbyte[1], inbyte[5], inbyte[2], inbyte[0], inbyte[3], inbyte[7], inbyte[4], inbyte[6]])

def finalper(inbyte): #permutacion final
	return([inbyte[3], inbyte[0], inbyte[2], inbyte[4], inbyte[6], inbyte[1], inbyte[7], inbyte[5]])

def keypermutation(inkey): #permutacion para la llave
	return([inkey[2], inkey[4], inkey[1], inkey[6], inkey[3], inkey[9], inkey[0], inkey[8], inkey[7], inkey[5]])

def splitkey(inkey): #funcion para dividir cualquier lista en dos y regresa tupla con los dos fragmentos
	key_l = [inkey[x] for x in range(0,int(len(inkey)/2))]
	key_r = [inkey[x] for x in range(int(len(inkey)/2), len(inkey))]
	return key_l, key_r

def leftshift(inkey_l, inkey_r): #shift a la izquierda para dos listas
	inkey_l.append(inkey_l.pop(0))
	inkey_r.append(inkey_r.pop(0))

def subkey(inkey_l, inkey_r): #permutacion de los dos fragmentos para generar un subkey
	return([inkey_r[0], inkey_l[2], inkey_r[1], inkey_l[3], inkey_r[2], inkey_l[4], inkey_r[4], inkey_r[3]])

def mixing(key, bit_block): #bloque f, entra llave y bitblock de 4 bits que sera expandido a 8, sale un int representando 4 bits
	bit_block_expanded = int(''.join([bit_block[3], bit_block[0], bit_block[1], bit_block[2], bit_block[1], bit_block[2], bit_block[3], bit_block[0]]),2) #expansion
	morph_key = int(''.join(key),2) #se comienza a tratar los bits como int para hacer xor
	xor_expand = bit_block_expanded ^ morph_key #xor
	half1, half2 = splitkey(chartobyte(xor_expand)) #regresamos a forma de bit y se divide en dos fragmentos de 4 bits
	bit2_1 = s_zero[int(''.join([half1[0], half1[3]]),2)][int(''.join([half1[1], half1[2]]),2)] #se calcula la coordenada en sbox0
	bit2_2 = s_one[int(''.join([half2[0], half2[3]]),2)][int(''.join([half2[1], half2[2]]),2)] #lo mismo pero en sbox1
	fourbit_l = format(bit2_1, '02b')#se forza el formato de los bits a dos bits, 0-> 00  1-> 01 
	fourbit_r = format(bit2_2, '02b')
	fourbit = list(fourbit_l+fourbit_r) #se concatenan los bits y se convierte en lista
	fourbit[0], fourbit[1], fourbit[3] = fourbit[1], fourbit[3], fourbit[0] # se permutan los bits
	fourbit = ''.join(fourbit) #se vuelven string
	exit4bit = int(fourbit, 2) #se usa la representación decimal de 4 bits
	return exit4bit



lines = []
for line in fileinput.input():
	lines.append(line.replace('\n',''))

# character = 'k' #esto fue implementado por si las entradas eran caracteres o strings
# char_bit_list = chartobyte(character)

##cifrado
if lines[0] == 'E' : 
	char_bit_list = list(lines[2]) #transformamos el plaintext a lista
	char_bit_list = initialper(char_bit_list) #permutacion inicial
	Li = char_bit_list[0:4] #se crean fragmentos corresondientes a parte izquierda
	Ri = char_bit_list[4:8] #y a parte derecha del plaintext
	key_input = list(lines[1]) #transformamos la llave a lista
	key_input = keypermutation(key_input) #permutacion de llave
	keysi_l, keysi_r = splitkey(key_input) #se divide la llave
	leftshift(keysi_l, keysi_r) #se hace shift a la izquierda
	subkey_one = subkey(keysi_l, keysi_r) #obtenemos la subllave uno
	func_k_r1 = mixing(subkey_one, Ri) #evaluamos la funcion f
	Li=int(''.join(Li), 2) ^ func_k_r1 #xor del resultado de f con L
	Li, Ri = Ri, Li #se cambia Li y Ri
	leftshift(keysi_l, keysi_r) #doble left shift
	leftshift(keysi_l, keysi_r)
	subkey_two = subkey(keysi_l, keysi_r) #obtenemos subkey2
	func_k_r2 = mixing(subkey_two, chartobyte(Ri)[4:8]) 
	Li=int(''.join(Li), 2) ^ func_k_r2 #xor
	cyphtxt = ''.join(chartobyte(Li)[4:8]) + ''.join(chartobyte(Ri)[4:8]) #concatenamos Li y Ri, sus bits menos significativos, esto solo es por el manejo del padding que hace chartobyte
	cyphtxt = finalper(list(cyphtxt)) #permutacion final
	print(''.join(cyphtxt))

##descifrado 
else:
	char_bit_list = list(lines[2])
	char_bit_list = initialper(char_bit_list)
	Li = char_bit_list[0:4]
	Ri = char_bit_list[4:8]
	key_input = list(lines[1])
	key_input = keypermutation(key_input)
	keysi_l, keysi_r = splitkey(key_input)
	leftshift(keysi_l, keysi_r)
	subkey_one = subkey(keysi_l, keysi_r)
	leftshift(keysi_l, keysi_r)
	leftshift(keysi_l, keysi_r)
	subkey_two = subkey(keysi_l, keysi_r)
	func_k_r1 = mixing(subkey_two, Ri)
	Li=int(''.join(Li), 2) ^ func_k_r1
	Li, Ri = Ri, Li
	func_k_r2 = mixing(subkey_one, chartobyte(Ri)[4:8])
	Li=int(''.join(Li), 2) ^ func_k_r2
	cyphtxt = ''.join(chartobyte(Li)[4:8]) + ''.join(chartobyte(Ri)[4:8])
	cyphtxt = finalper(list(cyphtxt))
	print(''.join(cyphtxt))



