#coding:utf-8
import networkx as nx
import math
import csv
import random as rand
import sys
import matplotlib.pyplot as plt

def buildG(G, file_, delimiter_):
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in reader:
        G.add_edge(int(line[0]),int(line[1]))
        # print('边',int(line[0]),int(line[1]))

def CmtyStep(G):
    init_number_comp = nx.number_connected_components(G)
    number_comp = init_number_comp
    while number_comp <= init_number_comp:
        bw = nx.edge_betweenness_centrality(G)#计算所有边的边介数中心性
        print('bw',bw)
        if bw.values() == []:
            break
        else:
            max_ = max(bw.values())#将边介数中心性最大的值赋给max_
        for k, v in bw.items():#删除边介数中心性的值最大的边
            if float(v) == max_:
                G.remove_edge(k[0],k[1])
        number_comp = nx.number_connected_components(G)#计算新的社团数量

def GetModularity(G, deg_, m_):
    New_A = nx.adj_matrix(G)#建立一个表示边的邻接矩阵
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    #计算Q值
    comps = nx.connected_components(G)#建立一个组成的列表 
    print('Number of communities in decomposed G: %d' % nx.number_connected_components(G))
    Mod = 0#设定社团划分的模块化系数并设初始值为0
    for c in comps:
        AVW = 0#两条边在邻接矩阵中的值
        K = 0#两条边的度值
        for u in c:
            AVW += New_deg[u]
            K += deg_[u]
        Mod += ( float(AVW) - float(K*K)/float(2*m_) )#计算出Q值公式累加符号后的值
    Mod = Mod/float(2*m_)#计算出模块化Q值
    return Mod

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)#图中点的个数
    # print('nodes',nodes)
    nodes = list(nodes)
    B = A.sum(axis = 1)#将矩阵的每一行向量相加，所得一个数组赋给B，表示与每个点相关的边数
    for i in range(n):
        # print(nodes[i],type(nodes[i]))
        deg_dict[nodes[i]] = B[i, 0]#将该值存到索引是i的元组中
    return deg_dict

def runGirvanNewman(G, Orig_deg, m_):
    BestQ = 0.0
    Q = 0.0
    while True:    
        CmtyStep(G)
        Q = GetModularity(G, Orig_deg, m_)
        print("Modularity of decomposed G: %f" % Q)
        if Q > BestQ:
            BestQ = Q
            Bestcomps = nx.connected_components(G)
            BestG = nx.Graph()
            BestG = G
            print("Components:", Bestcomps)
            nx.draw_spring(BestG,node_size = 100,alpha = 0.5,edge_color = 'b',font_size = 9)
            plt.savefig('BestG.png')
            plt.clf()
        if G.number_of_edges() == 0:
            break
    if BestQ > 0.0:
        print("Max modularity (Q): %f" % BestQ)
        print("Graph communities:", Bestcomps)
    else:
        print("Max modularity (Q): %f" % BestQ)

def main():
    graph_fn = 'data.txt'
    G = nx.Graph()
    buildG(G, graph_fn, ',')

    n = G.number_of_nodes()#顶点数量
    A = nx.adj_matrix(G)#邻接矩阵
    print(A)
    m_ = 0.0#计算边的数量
    for i in range(0,n):
        for j in range(0,n):
            m_ += A[i,j]
    m_ = m_/2.0
    #计算点的度
    Orig_deg = {}
    Orig_deg = UpdateDeg(A, G.nodes())
    #调用算法
    runGirvanNewman(G, Orig_deg, m_)

if __name__ == "__main__":
    main()
