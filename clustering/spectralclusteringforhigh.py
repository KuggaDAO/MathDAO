from sklearn.cluster import SpectralClustering
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from randomwalk import *

# 画图画不好看
QA = True
QC = True
AC = True
savefigs = False

# read data
user = pd.read_csv('processed/users.csv', usecols=['Id', 'Reputation'])
user['Id'] = user['Id'].astype(int)
user_dict = user.set_index('Id').to_dict()['Reputation']

qa = pd.read_csv('highqa.csv', header=None, names=['user1','user2','time'])
qc = pd.read_csv('highqc.csv', header=None, names=['user1','user2','time'])
ac = pd.read_csv('highac.csv', header=None, names=['user1','user2','time'])


# form the adjacency_matrix
G = nx.Graph()
if QA:
    nodelist = list(qa['user1'])+list(qa['user2'])
    #G.add_nodes_from(nodelist)
    for _, row in qa.iterrows():
        user1 = row['user1']
        user2 = row['user2']
        G.add_edge(user1,user2)
if QC:
    nodelist = list(qc['user1'])+list(qc['user2'])
    #G.add_nodes_from(nodelist)
    for _, row in qc.iterrows():
        user1 = row['user1']
        user2 = row['user2']
        G.add_edge(user1,user2)
if AC:
    nodelist = list(ac['user1'])+list(ac['user2'])
    #G.add_nodes_from(nodelist)
    for _, row in ac.iterrows():
        user1 = row['user1']
        user2 = row['user2']
        G.add_edge(user1,user2)

adj = nx.to_numpy_array(G)
for gamma in np.linspace(0, 2, 11):
    for n_clusters in range(3,11):
        sc = SpectralClustering(n_clusters=n_clusters, gamma=gamma)
        sc.fit(adj)
        labels = sc.labels_
        cluster_labels = {key:value for key,value in zip(G.nodes, labels)}

        # plot with point size related to reputation
        # and color related to its cluster.
        node_size = [user_dict[node]*0.001 for node in G.nodes()]
        cluster_labels = {key:value for key,value in zip(G.nodes, labels)}
        node_color = [cluster_labels[node] for node in G.nodes()]
        colormap = plt.get_cmap('tab10') # 颜色映射
        pos = nx.spring_layout(G)  # 选择一种布局算法
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=colormap, alpha=0.8)
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        plt.axis('off')
        plt.title(f'gamma:{gamma}, n_clusters:{n_clusters}')
        plt.show()

        if savefigs:
            plt.savefig('cluserting'+str(n_clusters)+'.png',bbox_inches='tight')