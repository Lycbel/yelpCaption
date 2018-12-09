import json

menuList = open('menu.list','r')
for line in menuList:
    line = line.replace('\n','')
    f = open ('reviews/'+line+'.json','r',encoding='utf-8');
    out = open(line+".review",'w+',encoding="utf-8")
    res = f.read();
    obj = json.loads(res);
    data = [];
    for item in obj['reviews']:
        try:
            for ite in item['review']['pics']:
                out.write(ite['url']+'\n')
                out.write(ite['caption']+'\n')           
        except:
            #means no caption
            pass
    out.flush();
    out.close();    