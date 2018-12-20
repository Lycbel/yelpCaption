import gensim
from difflib import SequenceMatcher

def processPhrase(w, stop_words):
    wlist = gensim.utils.simple_preprocess(w)
    wlistWOstopwords = [w for w in wlist if not w in stop_words]
    return wlistWOstopwords

def misspellCheck(w1, w2):
    ratio = SequenceMatcher(None, w1, w2).ratio()
    return ratio >= 0.8

def naiveMatch(target, w):
    if target == w:
        return 1.0
    else:
        if abs(len(target)-len(w)) <= 2:
            if misspellCheck(target, w):
                return 0.5
    return 0.0

def naiveSimilarity(model, stop_words, target_phrase, caption):
    try:
        target_phrase_list = processPhrase(target_phrase, stop_words)
        caption_list = processPhrase(caption, stop_words)
        score = 0.0
        for token in target_phrase_list:
            sim_list = [naiveMatch(token, t) for t in caption_list]
            max_sim = max(sim_list)
            score += max_sim
        lent = len(target_phrase_list);
        if(len(target_phrase_list)>=3):
            lent = 3 + 0.3*(lent-3)
        return score/lent
    except:
        return 0.0

def getSimilarity1(model, stop_words, target_phrase, caption):
    try:
        target_phrase_list = processPhrase(target_phrase, stop_words)
        caption_list = processPhrase(caption, stop_words)
        score = 0;
        for token in target_phrase_list:
            try:
                sim_list = [model.similarity(token, t) for t in caption_list]
            except KeyError:
                sim_list = [naiveMatch(token, t) for t in caption_list]
            max_sim = max(sim_list)
            score = score + max_sim
        lent = len(target_phrase_list);
        if(len(target_phrase_list)>=3):
            lent = 3 + 0.3*(lent-3)
        return score/lent
    except:
        return 0.0

def getSimilarity2(model, stop_words, target_phrase, caption):
    try:
        target_phrase_list = processPhrase(target_phrase, stop_words)
        caption_list = processPhrase(caption, stop_words)
        score = 0.0
        for token in target_phrase_list:
            sim_list = [model.similarity(token, t) for t in caption_list]
            sub_score = sum(sim_list) / len(sim_list)
            score += sub_score
        return score/len(target_phrase_list)
    except:
        return 0.0

def getSimilarity3(model, stop_words, target_phrase, caption):
    try:
        target_phrase_list = processPhrase(target_phrase, stop_words)
        caption_list = processPhrase(caption, stop_words)
        score = 0.0
        for token in target_phrase_list:
            sim_list = [model.similarity(token, t) for t in caption_list]
            max_sim = max(sim_list)
            if len(sim_list) > 1:    
                sim_list.remove(max_sim)
                max_sim2 = max(sim_list)
                score += ( max_sim + max_sim2 ) / 2.0
            else:
                score += max_sim
        return score/len(target_phrase_list)
    except:
        return 0.0