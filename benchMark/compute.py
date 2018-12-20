import gensim
from textblob import TextBlob
from nltk.corpus import stopwords
from similarity import *

# parameters
weightOfSubject = 0.9
similarityFunction = getSimilarity1
#similarityFunction = naiveSimilarity
modelname = "mixed.model" # yelp_cbow11.model

# data paths
data_path = '../menu/'

stop_words = set(stopwords.words('english'))

# load model
fname = modelname
model = gensim.models.Word2Vec.load(fname)

# open file
def openMenu(bname):
    bmenu = data_path + bname
    fmenu = open(bmenu, 'r')
    content = fmenu.readline().strip()
    fmenu.close()
    content = content[2:-2]
    content = content.replace('"','\'')
    content = content.split("), (")
    content = [c[1:-1].split("', '") for c in content]

    return content

def openPicCaption(bname):
    bcaption = data_path + bname + ".review"
    fcaption = open(bcaption, 'r')
    pics = []
    line = fcaption.readline().strip()
    while line:
        pic = [line]
        line = fcaption.readline().strip()
        pic.append(line)
        line = fcaption.readline().strip()
        pics.append(pic)
    fcaption.close()
    captions = [p[1] for p in pics]
    return pics, captions

def toUrl(item):
    item = item.lower()
    item = item.replace(" ", "-")
    item = item.replace("&", "and")
    return item


# helper functions
def getPic(picList, caption):
    for p in picList:
        if caption == p[1]:
            return p[0]
    return 'not found'

def calculateScoreLinearInterpolation(subScore, detScore):
    return subScore*weightOfSubject + (1-weightOfSubject)*detScore

def setWeiget(menu):
    global weightOfSubject

    detail = TextBlob(menu[0][1])
    for d in menu:
        try:
            detail = TextBlob(d[1])         
            if not detail.detect_language() == "en":
                print("detail dropped.")
                weightOfSubject = 1.0
                break
            else:
                break
        except:
            continue


def getItem(bName, caption):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~main: ", bName)
    menu = openMenu(bName)
    #setWeiget(menu)

    score = 0.0
    topDish = ''
    for dish in menu:
        subject = dish[0]
        detail = dish[1]
        cur_score_subject = similarityFunction(model, stop_words, subject, caption)
        cur_score_detail = similarityFunction(model, stop_words, detail, caption)
        cur_score = calculateScoreLinearInterpolation(cur_score_subject, cur_score_detail)
        if cur_score >= score:
            score = cur_score
            topDish = subject

    return topDish, score

# main function
def main(bName, max_score=False, top_three=False):
    # open menu & captions
    menu = openMenu(bName)
    setWeiget(menu)
    pics, captions = openPicCaption(bName)

    rs_dict = {}
    for caption in captions:
        score = 0.0
        topDish = ''
        for dish in menu:
            subject = dish[0]
            detail = dish[1]
            target = subject + ', ' + detail
            cur_score_subject = similarityFunction(model, stop_words, subject, caption)
            cur_score_detail = similarityFunction(model, stop_words, detail, caption)
            cur_score = calculateScoreLinearInterpolation(cur_score_subject, cur_score_detail)
            if cur_score >= score:
                score = cur_score
                topDish = target
        if score >= 0.6:
            if max_score:
                if topDish not in rs_dict.keys():
                    rs_dict[topDish] = [caption, getPic(pics, caption)]
                else:
                    if score >= rs_dict[topDish][1]:
                        rs_dict[topDish] = [caption, getPic(pics, caption)]
            elif top_three:
                if topDish not in rs_dict.keys():
                    rs_dict[topDish] = [caption, getPic(pics, caption)]
                else:
                    pic_ = getPic(pics, caption)
                    if len(rs_dict[topDish]) < 4 and pic_ != rs_dict[topDish][1]:
                        rs_dict[topDish] += [caption, pic_]
                    elif len(rs_dict[topDish]) >= 4 and len(rs_dict[topDish]) < 6:
                        if pic_ != rs_dict[topDish][3] and pic_ != rs_dict[topDish][1]:
                            rs_dict[topDish] += [caption, pic_]
            else:
                if topDish not in rs_dict.keys():
                    rs_dict[topDish] = ['--'+caption+' >>> '+str(score)+' >>> '+getPic(pics, caption)]
                else:
                    rs_dict[topDish].append('--'+caption+' >>> '+str(score)+' >>> '+getPic(pics, caption))
    for r in rs_dict.items():
        if not max_score:
            print('===>', r[0])
            for l in r[1]:
                print(l)
            print()
        else:
            print('===>', r[0])
            print("    ", r[1])
            print()
    return rs_dict


