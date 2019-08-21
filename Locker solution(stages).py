# state before students enter
state0 = [False for i in range(100)]
print(state0,'\n')

# state after first student passes
state1 = []
for locker in state0:
    locker1 = not locker
    state1.append(locker1)
print(state1,'\n')

# state after second student passes
state2 = []
count = list(enumerate(state1))
for item in count:
    if item[0] == 0:
        state2.append(item)
    else:
        state2.append((item[0], not item[1]))
print(state2, '\n')

# state after other students pass
final = state2.copy()
for n in range(2,100):
    for item in final:
        if item[0] % n == 0:
            final[item[0]] = (item[0], not item[1])
        else:
        	 final[item[0]] = (item[0], item[1])
print(final, '\n')

# creation of list containing locker numbers with value True i.e open
result = []
for item in final:
	if item[1] == True:
		result.append('L'+str(item[0]+1))
print(result, '\n')

# creation of string showing open lockers with one-space spacing
print(' '.join(result))
