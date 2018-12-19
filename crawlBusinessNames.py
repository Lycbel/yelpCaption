import urllib3,certifi
import re
import html
import sys
import os.path
import config
import time
#https://www.yelp.com/search?find_desc=&find_loc=IL&ns=1&start=10
mainPre =config.mainPre
restPerPage = config.restPerPage #restraunt number each page in main page
restChunckSize = config.restChunckSize #each file contain how many res
startc = config.checkForCrawlTotal();
logFile = config.logfile
ppc = 200 #200 res print one message
lf = open(logFile,'a+');
    
def pLog(strc):
    print(strc);
    sys.stdout.flush()
    lf.write(strc+'\n')
    lf.flush();
def download_content_by_url(url):
    time.sleep(1.1)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
    response = http.request('GET', url)
    return html.unescape(response.data.decode('utf-8')).replace('\n','').replace('\r','')
def downloadMainPageChunck(start,restChunckSize):
    finalResult = []
    fileStart = start + 1;
    fileEnd = start + restChunckSize;
    fileName = config.chunckFolder+'chunck_'+str(fileStart)+'_'+str(fileEnd);
    if (os.path.isfile(fileName)):
        pLog("warning duplicated rest name file:" + fileName);
    f = open(fileName,'w+');
    for i in range(0,int(restChunckSize/restPerPage)):
        #load 10 res
        print(mainPre+str(start))
        sys.stdout.flush()
        page = download_content_by_url(mainPre+str(start))
        res = re.compile('link__373c0__29943 photo-box-link__373c0__1AvT5 link-color--blue-dark__373c0__1mhJo link-size--default__373c0__1skgq" href="/biz/(.*?)" target=')
        result = res.findall(page)
        for ele in result:
            finalResult.append(ele);
        start = start + restPerPage;
    for ele in finalResult:
        f.write(ele+'\n');
    f.close();
    if(config.storeStart(start)):
        pLog ('finished start with:'+str(start-restChunckSize))
    else:
        pLog('error start with:'+str(start-restChunckSize))
        sys.exit(0)
    return start;    
def job(rounds=config.maxRoundOfJob):
    global startc
    pLog('start job')
    for i in range(0,rounds):
       start = downloadMainPageChunck(startc,restChunckSize);
       startc = start;
       print('finish one chunck')
    pLog('end job') 
    lf.close();
job();    
           
           

