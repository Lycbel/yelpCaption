infile = ['cafe-ba-ba-reeba-chicago-3','wildberry-pancakes-and-cafe-chicago-2']

for item in infile:
	f = open(item+'.bench0','r',encoding='utf-8')
	fo = open(item+'.bench','w+',encoding='utf-8')
	cc = 0;
	for lin in f:
		cc = cc % 3;
		cc = cc+1;
		if(cc==2):
			continue
		fo.write(lin);	
	f.close();
	fo.close();