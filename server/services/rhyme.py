from random import random
from re import X

from server.services.ml import is_rhyming



def check_rhyme(poem):
    words_in_para = []
    intra_paragraph = []
    paras = poem.split("\n\n")
    x = 1

    # in paragraph
    for para in paras:
        all_clusters = []
        this_words = []
        lines = para.split("\n")
        for line in lines:
            words = line.split(" ")
            this_words.extend(words[max(-len(words),-2):])
        words_in_para.append(this_words)
        n = len(this_words)
        s = set()
        for i in range(n):
            if i in s:
                continue
            s.add(i)
            clus = [this_words[i]]
            for j in range(i + 1, n):
                if j not in s and is_rhyming(this_words[i], this_words[j]):
                    # s.add(j)
                    clus.append(this_words[j])
            if(len(clus)>1):
                all_clusters.append(clus)
    
        c_map = {}
        for i in range(len(all_clusters)):
            clus = all_clusters[i]
            for word in clus:
                c_map[word] = x
            x+=1
        

        lines = para.split("\n")
        _lines = []
        for line in lines:
            words = line.split(" ")
            _words = []
            for i in range(len(words)):
                word = words[i]
                _words.append({'text':word, 'class': (c_map[word] if word in c_map and len(words)-i < 2 else 0) })
            _lines.append(_words)
        intra_paragraph.append(_lines)


    # inter-paragraph
    inter_paragraph = []
    all_clusters = []
    for i in range(len(paras)-1):
        this_words = words_in_para[i]
        other_words = []
        for j in range(0, len(paras)):
            if(i!=j):
                other_words.extend(words_in_para[j])
        n = len(this_words)
        nn = len(other_words)
        s = set()
        for i in range(n):
            if i in s:
                continue
            s.add(this_words[i])
            clus = [this_words[i]]
            for j in range(nn):
                if other_words[j] not in s and is_rhyming(this_words[i], other_words[j]):
                    clus.append(other_words[j])
            if(len(clus)>1):
                all_clusters.append(clus)
    
    c_map = {}
    x = 1
    for i in range(len(all_clusters)):
        clus = all_clusters[i]
        for word in clus:
            c_map[word] = x
        x+=1
    

    for i in range(len(paras)):
        lines = paras[i].split("\n")
        _lines = []
        for line in lines:
            words = line.split(" ")
            _words = [] 
            for i in range(len(words)):
                word = words[i]
                _words.append({'text':word, 'class': (c_map[word] if word in c_map and len(words)-i < 3 else 0) })
            _lines.append(_words)
        inter_paragraph.append(_lines)

    return {"intra_paragraph":intra_paragraph, "inter_paragraph":inter_paragraph}