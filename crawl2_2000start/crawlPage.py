import urllib3,certifi
import re
import html
import sys
import json
import config
import os.path
import time
import crawlMenu as cm
lf = open(config.reviewLogFile,'a+');
reviewTotalFile = open('rtotal.txt','a+',encoding='utf-8')
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
def pLog(strc):
    print(strc);
    sys.stdout.flush()
    lf.write(strc+'\n')
    lf.flush();   

def download_content_source(url):
    tim0 = time.time();
    response = http.request('GET', url)
    tim1 = time.time();
    time01=tim1-tim0;
    result = response.data.decode('utf-8');
    result = html.unescape(re.sub(r'\\u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), result))
    time.sleep(1.5);
    print("download time:" +str(time01) + "url:"+url)
    sys.stdout.flush();
    return result.replace("\\n","").replace('\\"','"').replace('\n','').replace('\r','')
resPic = re.compile('<li style=.*?</li>');
rehttp =re.compile('https://.*?\.jpg');
recap = re.compile('photo-box-overlay_caption">(.*?)</div>');
def get_pic(review_raw):
    pics = []
    result = resPic.findall(review_raw);
    for ele in result:
        url = rehttp.search(ele);
        url = url.group()
        try:
            cap = recap.search(ele);
            cap = cap.group(1);
        except:#no caption ignore the pic
            #traceback.print_exc(file=sys.stdout)
            url = None;
            cap = None;
        if (url!=None):
            pic = {'url':url,'caption':cap}
            pics.append(pic)
    if(pics==[]):
         pics = None;
    return pics
resReview = re.compile('<p lang="en">(.*?)</p>');
def get_review(review_raw):
    try:
        result = resReview.search(review_raw);
        des = result.group(1);
    except Exception:
        pLog('no review content')
        return None
    return des
def get_reviews(page):
    res = re.compile('<div class="review-content">.*?<div class="review-footer clearfix">');
    result = res.findall(page);
    reviews = []
    for ele in result:
        des = get_review(ele)
        reviewTotalFile.write(des+'\n');
        pics = get_pic(ele)
        reviews.append({'review':{'des':des,'pics':pics}})
    reviewTotalFile.flush();
    return reviews   
   
def download_page_by_start(name,start):
    url = 'https://www.yelp.com/biz/'+name+'/review_feed/?start='+str(start);
    page = download_content_source(url) 
    return page
def job(chunkFileName):
    chunkFile = config.chunckFolder+chunkFileName;
    reviewChunkFolder = config.reviewFolder+chunkFileName+'/'
    if(os.path.isdir(reviewChunkFolder)):
        pLog('already have the chunck folder')
    else:
        os.mkdir(reviewChunkFolder)
    f = open(chunkFile);
    for i in f:
        name = i.replace('\n','')
        fileName = reviewChunkFolder+name+'.json'
        menu = cm.loadMenuByName(name);
        if(menu==None):
            pLog('this business doesn\'t have menu:'+name)
            continue;
        if(os.path.isfile(fileName)):
            pLog('already have the file:'+fileName)
            #todo maybe merge new
        else:
            pLog('start crawl the restaraunt:' + name)
            result = [];
            start = config.reviewStart;
            for it in range(0,config.reviewRounds):
                tresult = get_reviews(download_page_by_start(name,start));
                if(tresult!=[]):
                    result = result + tresult;
                    start = start + config.reviewEach;
                else:
                    pLog('no result at round: '+str(it))
                    result = {'name':name,'reviews':result}
                    f1 = open(fileName,'w+',encoding='utf-8')
                    f1.write(json.dumps(result,ensure_ascii=False));
                    f1.flush;
                    f1.close();
                    break;
            if(result==[]):
                pLog('error no result from this rest: '+name)
                break;
            result = {'name':name,'reviews':result}
            #todo  maybe merge new
            f1 = open(fileName,'w+',encoding='utf-8')
            f1.write(json.dumps(result,ensure_ascii=False));
            f1.flush;
            f1.close();
    f.close();         
jobName = ['chunck_1_500','chunck_501_1000'];            
job(jobName[0])    
#job(jobName[1])  
#print(get_reviews(download_page_by_start("wildberry-pancakes-and-cafe-chicago-2",0)) )          
def download_content_sourcem():
    f = open('test/b.test','r',encoding='utf-8')
    return f.read();    

#cpm = json.dumps(get_reviews(download_content_sourcem()),ensure_ascii=False) 
#print(cpm)           
def storeTestHtml():    
    f = open('test/c.test','w',encoding='utf-8')
    f.write(download_content_source('https://www.yelp.com/biz/beatrix-streeterville-chicago'))  
    f.flush();
    f.close()  