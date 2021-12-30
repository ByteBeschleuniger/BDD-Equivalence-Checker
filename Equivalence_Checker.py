
#-------------------------------------------------------------------------------
# Project       : Equivalence Checker (BDD)
#-------------------------------------------------------------------------------
# File          : Equivalence_Checker
# Author        : Rahul Kumar Singh
# University    : TU-Chemnitz, 
# Created       : 2021-04-12
# Last update   : 2021-16-28

#-------------------------------------------------------------------------------
# Description: Gate level netlist equivalence checker using Binary Decision Diagrams
#-------------------------------------------------------------------------------


import sys
import collections

def readNetlist(file):
    nets = int(file.readline())
    inputs = file.readline().split()
    inputs.sort()
    outputs = file.readline().split()
    outputs.sort()

    # read mapping
    mapping = {}
    while True:
        line = file.readline().strip()
        if not line:
            break

        net, name = line.split()
        mapping[name] = int(net)

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        #ports = map(int, bits)
        ports = [int(port) for port in bits]
        gates.append((gate, ports))

    return inputs, outputs, mapping, gates


# read netlists
inputs1, outputs1, mapping1, gates1 = readNetlist(open(sys.argv[1], "r"))
inputs2, outputs2, mapping2, gates2 = readNetlist(open(sys.argv[2], "r"))

#Code!!
BDD_empty = {}
map_1 = {}
map_2 = {}

def NETLIST_1(inputs, gates):

	for input in inputs:
		var_bdd = BDD(input,True,False)
		var = mapping1[input]
		map_1[var] = var_bdd

	for gate in gates:			#ITE form for gates

		if gate[0] == 'inv':
			map_1[gate[1][1]] = ITE(map_1[gate[1][0]], False, True)
		elif gate[0] == 'or':
			map_1[gate[1][2]] = ITE(map_1[gate[1][0]], True, map_1[gate[1][1]])
		elif gate[0] == 'and':
			map_1[gate[1][2]] = ITE(map_1[gate[1][0]], map_1[gate[1][1]], False)
		elif gate[0] == 'xor':
			map_1[gate[1][2]] = ITE(map_1[gate[1][0]], ITE(map_1[gate[1][1]], False, True), ITE(map_1[gate[1][1]], True, False))




def NETLIST_2(inputs, gates):

	for input in inputs:
		var_bdd = BDD(input,True,False)
		var = mapping2[input]
		map_2[var] = var_bdd

	for gate in gates:			#ITE form for gates

		if gate[0] == 'inv':
			map_2[gate[1][1]] = ITE(map_2[gate[1][0]], False, True)
		elif gate[0] == 'or':
			map_2[gate[1][2]] = ITE(map_2[gate[1][0]], True, map_2[gate[1][1]])
		elif gate[0] == 'and':
			map_2[gate[1][2]] = ITE(map_2[gate[1][0]], map_2[gate[1][1]], False)
		elif gate[0] == 'xor':
			map_2[gate[1][2]] = ITE(map_2[gate[1][0]], ITE(map_2[gate[1][1]], False, True), ITE(map_2[gate[1][1]], True, False))


def BDD(var, left, right):
	if (left == right):				#Elimination
		return left
	else:						#Merge
		if (var, left, right) in BDD_empty:
			return BDD_empty[(var, left, right)]
		else:
			BDD_empty[(var, left, right)] = (var, left, right)
			return BDD_empty[(var, left, right)]

def ITE(f,g,h):
	if f == 1:				#Trivial Cases
		return g	

	if f == 0:
		return h

	if g == h:
		return g

	if g == 1 and h == 0:
	        return f

	else:					#Distinction Case

	        Top_var = f[0]
	        if (g is not True) and (g is not False) and (g[0] < Top_var):
			Top_var = g[0]
		if (h is not True) and (h is not False) and (h[0] < Top_var):
			Top_var = h[0]

		f1, f0 = COFACTORS(f, Top_var)
		g1, g0 = COFACTORS(g, Top_var)
		h1, h0 = COFACTORS(h, Top_var)

		left = ITE(f1, g1, h1)        			  #Generate left and right branches
		right = ITE(f0, g0, h0)

		return BDD(Top_var, left, right)		  #Build BDD


def COFACTORS(f, x):
	if f == 1:		         #Trivial Cases
		return True,True

	elif f == 0:
		return False, False

	else:				#Distinction Case
		if f[0] == x:
			Cof_1, Cof_0 = f[1], f[2]

		elif f[0] > x:
			Cof_1, Cof_0 = f, f

		else:
			left_0, left_1 = COFACTORS(f[1], x)
			right_0, right_1 = COFACTORS(f[2], x)


			Cof_1 = BDD(x, left_1, right_1)
			Cof_0 = BDD(x, left_0, right_0)
	return Cof_1, Cof_0





NETLIST_1(inputs1, gates1)
NETLIST_2(inputs2, gates2)

flag = 0
v1 = []
v2 = []

for output in outputs1:
	val1 = mapping1[output]
	v1.append(val1) 
	#print(val1)
for output in outputs2:
	val2 = mapping2[output]
	v2.append(val2) 
	#print(val2)
count = len(v1);                       #Note - v1 and v2 have similar number of items
i=0
while (i < count):
 
	if(map_1[v1[i]] == map_2[v2[i]]):#collections.Counter(map_1[v1])==collections.Counter(map_2[v2])):
		print("Equal now")
		
	else:
		print("Unequal now")
		flag = flag+1
	i=i+1;

print("\n")
if flag < 1:
	print("Final Result : Yes, Equivalent\n")
else:
	print("Final Result : No, Not Equivalent\n")




