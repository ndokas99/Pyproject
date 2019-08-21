import re
from datetime import timedelta


# open file
file = input('Enter smi filename: ')
with open('smi input/'+file+'.smi', 'r') as f:
	ent = f.read()

# quotation correction
ent1 = re.sub(r'&#39;', "'", ent)
ent2 = re.sub(r'&#40;', '"', ent1)

# define search for times
a = re.findall(r'Start=[\d]+', ent2)

# add times to list
b = [(re.search(r'[\d]+', item)).group() for item in a]
	
# convert times to desired format
d = []
for item in b:
	e = timedelta(milliseconds=int(item))
	if re.search(r'[.]', str(e)) is None:
		f = str(e)+'.000'
	else:
		f = str(e)
	d.append(f[0:11])
	
time = list(enumerate(d))
			
# content seeking
ent3 = re.findall(r'(?<=SYNC\s)Start=.*?<SYNC|(?<=SYNC\s)Start=.*?</body', ent2, re.DOTALL)

# filter and concatenation of strings
ent4 = [re.sub(r'\n', ' ', item) for item in ent3]
ent5 = []
for item in ent4:
	a = re.findall(r'>.*?<', item)
	b = [c for c in a if c != '><']
	d = []
	for e in b:
		f = re.search(r'[^>].*[^<]', e)
		# filter of None values
		if bool(f) is True:
			d.append(f.group())
		else:
			continue
	g = ''.join(d)
	ent5.append(g)

# writing to output file
with open('srt output/'+file+'.srt', 'w') as f:
	def content(string):
		"""Yield of content to file"""
		for item in string:
			if bool(re.match(r'.+', item)) is not True:
				yield '......'
			else:
				yield item
				
				
	for tim, cont in zip(time, content(ent5)):
		# iteration correction for last
		if tim[0] == len(time)-1:
			var1 = re.sub(r'[0-5][0-9]\Z', '58', tim[1])
			var2 = re.sub(r'[0-5][0-9][^:\d]', '59.', var1)
			f.write(str(tim[0]+1)+'\n')
			f.write(tim[1]+' --> '+var2+'\n')
			f.write(cont+'\n')
			print('Progress: 100.00% ==> Complete')
			break
		# writing of srt file
		f.write(str(tim[0]+1)+'\n')
		f.write(tim[1]+' --> '+time[tim[0]+1][1]+'\n')
		f.write(cont+'\n\n')
		# Terminal output
		if tim[0] == 0:
			print('CONVERTING')
		print('Progress: {0:.2%}'.format(tim[0]/(len(time)-1)))
