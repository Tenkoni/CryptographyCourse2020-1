#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput

lines = ["ENCRYPT","PDRRNGBENOPNIAGGF"]
#for line in fileinput.input():
# 	lines.append(line.replace('\n',''))
abc = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
dict_creator = []
y_axis = -1;

##generacion primera parte tabla
for index, cha in enumerate(lines[0]):
	if index%5 == 0:
		y_axis += 1
	dict_creator.append((cha, (y_axis,index%5)))
##generacion relleno de tabla
for index, cha in enumerate(abc):
	if cha not in lines[0]:
		if ((dict_creator[-1][1][1])+1)%5 == 0:
			y_axis += 1
		dict_creator.append((cha, (y_axis, (dict_creator[-1][1][1]+1)%5)))

table = dict(dict_creator)


##bloque de cifrado
if ' ' in lines[1]:
	cyphertext_h = []
	cyphertext_l = []
	for char in lines[1].replace(' ', ''):
		cyphertext_h.append(table[char][0])
		cyphertext_l.append(table[char][1])
	cyphercode = cyphertext_h + cyphertext_l
	print(cyphertext_h)
	print(cyphertext_l)
	cypher_iter = iter(cyphercode)
	cyphertext = []
	for index in range(len(cyphertext_l)):
		a = next(cypher_iter)
		b = next(cypher_iter)
		cyphertext.append(list(table.keys())[list(table.values()).index((a,b))])

	print(''.join(cyphertext))

else:
##bloque de decifrado
	decrypt_code = []
	plain_text = []
	for char in lines[1]:
		decrypt_code.append(table[char][0])
		decrypt_code.append(table[char][1])
	print(decrypt_code)
	for x in range(int(len(decrypt_code)/2)):
		print([decrypt_code[x], decrypt_code[int(x+len(decrypt_code)/2)]])
		plain_text.append(list(table.keys())[list(table.values()).index((decrypt_code[x],decrypt_code[int(x+len(decrypt_code)/2)]))])
	print(''.join(plain_text))


