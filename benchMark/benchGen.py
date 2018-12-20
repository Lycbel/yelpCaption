import sys
import compute 
caption = True;

f = ['smoque-bbq-chicago','wildberry-pancakes-and-cafe-chicago-2','the-purple-pig-chicago','portillos-hot-dogs-chicago-4','cafe-ba-ba-reeba-chicago-3']
countT  = 0;
countC = 0;
for lin in f:
    lin = lin.replace('\n','')
    inFile = 'data/'+lin+'.bench'
    inf = open(inFile,'r',encoding = 'utf-8')
    caps = []
    menu = [];
    for line in inf:
        if(line=='\n'):
            break
        line = line.replace('\n','')
        if(caption):
            caps.append(line)
        else:
            menu.append(line)    
        caption = not caption;    
    inf.close();
    ofile = 'data/'+lin+'.bench1'
    of = open(ofile,'w+',encoding = 'utf-8')
    for i in range(0,len(caps)):
        gme = compute.getItem(lin,caps[i])[0]
        tme = menu[i];
        tme = str.lower(tme)
        gme = str.lower(gme)
        if(gme in tme):
            countC = countC+1;
        else:
            of.write(caps[i]+'\n')
            of.write(tme+'\n')
            of.write(gme+'\n\n\n')    
        countT = countT+1;
    of.close(); 
print('c'+str(countC)+'t'+str(countT))