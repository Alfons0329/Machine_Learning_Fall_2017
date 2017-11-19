import sys

try:
	fp_in = open("output.txt", "r")
except(IOError):
	print('Error: can\'t open "output.txt"!!\n')
	sys.exit()
try:
	fp_ans = open("answer.txt", "r")
except(IOError):
	print('Error: can\'t open "output.txt"!!\n')
	sys.exit()

# get data that we need to check is it correct
get_data = [instance.split(' ') for instance in fp_in.read().split('\n')[:-1]]
tmp_len = len(get_data)
for i in range(tmp_len):
	if get_data[tmp_len-i-1][0] == '' or get_data[tmp_len-i-1][0] == 'KNN':
		del get_data[tmp_len-i-1]
# turn string to int
for i in range(len(get_data)):
	for j in range(len(get_data[i])-1):
		get_data[i][j] = int(get_data[i][j])

# get answer
ans_data = [instance.split(' ') for instance in fp_ans.read().split('\n')[:-1]]
tmp_len = len(ans_data)
for i in range(tmp_len):
	if ans_data[tmp_len-i-1][0] == '' or ans_data[tmp_len-i-1][0] == 'KNN':
		del ans_data[tmp_len-i-1]
# turn string to int
for i in range(len(ans_data)):
	for j in range(len(ans_data[i])-1):
		ans_data[i][j] = int(ans_data[i][j])

# compare two data
if len(ans_data) != len(get_data):
	print("Error!! Two data have different size!!\n")
	sys.exit()
else:
	for i in range(len(ans_data)):
		if len(ans_data[i]) != len(get_data[i]):
			print("Wrong!!", i, end='')
			print()
			sys.exit()
		else:
			for j in range(len(ans_data[i])):
				if ans_data[i][j] != get_data[i][j]:
					print("Wrong!!", i, ',','ans =', ans_data[i][j], 'get =', get_data[i][j] , end='')
					print()
					sys.exit()

print("Correct!!")	
