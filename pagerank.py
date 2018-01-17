# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:19:40 2017

@author: DART_HSU
"""

import numpy as np
from scipy.sparse import csc_matrix
import re
from operator import itemgetter

def pageRank(G, s = .85, maxerr = .0001):
    n,d  = G.shape

    # compute pagerank r until it converge
    ro, r = np.zeros(n), np.ones(n)

    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each item's pagerank at a time
        for i in range(0,n):
            Ai = 0 
            
            for j in range(0,n):
                if (sum (G[j])!=0):
                    Ai += ro[j] * G[j][i] / sum (G[j])
                    
            r[i] = Ai*s + (1-s)
                
    return r/float(sum(r))

def read_txt(file_name):
    f = open(file_name, 'r')
    list_txt = []

    for line in f :
        list_txt.append (re.sub("\d+\t+|\d+\s+|,|\n","",str(line)))
        
    f.close()

    return list_txt

def read_node_txt(file_name, shape):
    f = open(file_name, 'r')
    node_links = np.zeros((shape, shape), dtype=np.int)
    index_node_list = []

    for line in f :
        items = []
        for item in line.split(' ')[1:]:
            item = item.replace(',', '').replace('\n', '').replace('\t', '')
            if item != '':
                items.append(int(item)-1)
        index_node_list.append (items)
    
    index = 0
    for item in index_node_list:
        for node in item:
            node_links[index][node] = 1
        index += 1
    
    f.close()
    
    return node_links    

if __name__=='__main__':
    #read unitlisting.txt, and process digtal & tab & space
    pagerankbusiness = read_txt('unitlisting.txt')
    #read nodelink.txt
    node_links = read_node_txt('nodelinks.txt', len(pagerankbusiness))

    #combine score & node name
    pagerank_nodes = zip(pagerankbusiness, pageRank(node_links))
    pagerank_nodes = sorted(pagerank_nodes, key=itemgetter(1), reverse=True)
    
    print ('Welcome to PageRank!')

    while(1):
        print ("請選擇操作模式\n輸入'1'－顯示Top數量\n輸入'2'－顯示搜尋文字\n輸入'3'－離開")
        operator = input("Input:")

        if operator == '3' :
            break;
        elif operator == '2' :
            search_s = input("Please input search string ：")

            for title, score in pagerank_nodes:
                if search_s in title :
                    print (title + ', score: ' + str(score) )
            
        elif operator == '1' :
            top_num = int ( input("Please input the top number displayed ：") )
           
            for i in range(top_num):
                print (pagerank_nodes[i])

    print ('Thank you for your using!')