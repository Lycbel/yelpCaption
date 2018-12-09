import urllib3,certifi
import re
import html
import time
def download_content_source(url):
    tim = time.time()
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    result= html.unescape(response.data.decode('utf-8')).replace('\n','').replace('\r','')
    print('time+'+str(time.time()-tim))
print('start')
download_content_source('https://www.yelp.com/biz/beatrix-river-north-chicago?page_src=related_bizes')
