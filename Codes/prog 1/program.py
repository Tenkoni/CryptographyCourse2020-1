import fileinput

def convert(inputs):
	try:
		return int(inputs)
	except:
		return float(inputs)

lines = []
for line in fileinput.input():
	lines.append(line)

ans = 0
for line in lines:
	ans += convert(line)

print(ans)