import re
input = ['the-purple-pig-chicago']

for item in input:
	inf = open(item+'.review','r',encoding='utf-8')
	of = open(item+'.bench','w+',encoding='utf-8')
	count = True;
	matched = ''
	for lin in inf:
		if count:
			lin = lin.replace('\n','')
			res = re.compile('"(.*?)"')
			result = res.findall(lin)
			final = ''
			first = True
			for i in result:
				if first:
					final  = i;
					first = False;
				else:	
					final = final +'#' + i
			matched = final;		
		else:
			pass
			if(matched!=''):
				of.write(lin);
				of.write(matched+'\n');
		count = not count	
	of.close()
	inf.close()		