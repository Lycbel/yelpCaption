import urllib3,certifi
import re
import html
import sys
import json
replace = [['\'',''],['&','and'],[',','']];
#todo filter out restraunt without menue
def download_content_source(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
    response = http.request('GET', url)
    return html.unescape(response.data.decode('utf-8')).replace('\n','').replace('\r','')
    #return response.data.decode('utf-8').replace('\n','').replace('\r','');

def getMenu(content):
    res = re.compile('<div class="arrange_unit arrange_unit--fill menu-item-details">.*?</div>');
    result = res.findall(content);
    if(result==[]):
        return None
    results = []
    for item in result:
        results.append(getItem(item))
    return results    

def getItem(itemc):
    try:
        res = re.compile('(<p.*?>)(.*?)</p>');
        result = res.search(itemc);
        des=result.group(2)
    except Exception:
        des="" # means no description
    try:
        res = re.compile('(<a.*?>)(.*?)</a>');
        result = res.search(itemc);
        title=result.group(2)
    except Exception:
        #may not have <a>
        try:
            res = re.compile('<h4> *(.*?) *</h4>');
            result = res.search(itemc);
            title=result.group(1)
        except Exception:
            title="error"
    return (title,des)    
def loadMenue(infile,manuListFile):
    f = open(infile,'r',encoding='utf-8');
    m = open(manuListFile,'a+',encoding='utf-8')
    i = 0;
    lastMenu = None;
    cando = False;
    for lin in m:
        lastMenu = lin;    
    for line in f:
        line = line.replace('\n','')
        if(i>10):
            f.close();
            m.close();
            sys.exit(0);
        if(lastMenu != None):
            if(lastMenu == line):
                cando = True;
            if(not cando):
                print('alrady have menu of res:' + line)
                continue
        else:
            pass
            
        url = 'https://www.yelp.com/menu/'+line
        result = getMenu(download_content_source(url))
        if (result != None):
            fileName = 'menu/'+line
            fo = open(fileName,'w+',encoding='utf-8');
            i = i + 1;
            result = str(result)+'\n\n'
            fo.write(result)
            fo.flush();
            fo.close();
            m.write(line+'\n')
            m.flush();
            print("okay"+line)
    f.close();    
infile = "chunck/chunck_1_500"
loadMenue(infile,'menu.list')
#print(getMenu(download_content_source('https://www.yelp.com/menu/wildberry-pancakes-and-cafe-chicago-2')))
 
    
    
