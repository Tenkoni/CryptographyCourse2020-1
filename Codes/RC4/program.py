#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fileinput

##RC4
##MIRAMONTES SARABIA LUIS ENRIQUE
##CARVENTE VELASCO CARLOS ALBERTO

def KSA(key):
	key = [ord(char) for char in key]
	S=[]
	for i in range(0, 256):
		S.append(i)
	j = 0
	for i in range (0, 256):
		j = (j + S[i] + key[i % len(key)]) % 256
		S[i], S[j] = S[j], S[i]
	return S

def PRGA(S, i, j):
	i = (i + 1) % 256
	j = (j + S[i]) % 256
	S[i], S[j] = S[j], S[i]
	return S[(S[i]+S[j]) % 256], i, j ##regresa byte K, luego indices

lines = []
for line in fileinput.input():
	lines.append(line.replace('\n',''))

output_stream = ""
keystream = KSA(lines[0])
i = 0
j = 0
for char in lines[1]:
	prga, i, j = PRGA(keystream, i, j)
	output_stream += str(format((ord(char) ^ prga), 'x').zfill(2)).upper()

print(output_stream)