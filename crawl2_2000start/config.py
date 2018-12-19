#for search main
import traceback
import sys
import time
mainPre ='https://www.yelp.com/search?find_desc=&find_loc=IL&ns=1&start='
restPerPage = 10 #one time how many res in one page
maxRoundOfJob = 2; # will how many chuncks to produce this run 
logfile = "main.log"
startfile = 'start.start'
def checkForCrawlTotal():
    try:
        f = open("start.start",'r');
        i = f.readline();
        start = int(i);
        f.close();
    except Exception:
        print('can\'t get start in start.start, please to make sure you have start.start and correct start number in it');     
    return start;
def storeStart(i):
    try:
        f = open("start.start",'w');
        f.write(str(i));
        f.flush()
        f.close();
        return True
    except:
        print('fatal can\'t save start:'+str(i)); 
        traceback.print_exc(file=sys.stdout)
        return False
    
#for load review
#name will be chunck_start_end  chunck_10_20 means 10-20 11 restraunts, and  first restraunt is indexed 1
restChunckSize = restPerPage * 50  #each file contain how many res    
chunckFolder = 'chunck/'
reviewRounds = 100;
reviewEach = 20;
reviewFolder = 'review/'
reviewLogFile = 'review.log'
reviewStart = 2000 ;