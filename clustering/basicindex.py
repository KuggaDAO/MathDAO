import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import numpy as np

from randomwalk import *

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

# 连通性
components = list(nx.connected_components(G))
num_com = len(components) # num
largest_component = max(components, key=len)
largest_component_size = len(largest_component)
ratio = largest_component_size/G.number_of_nodes() # largest/total nodes
degrees = [degree for _, degree in G.degree()]
mean_degree = np.mean(degrees)
std_degree = np.std(degrees) # std of degrees
print("连通分支数目:", num_com)
print("最大连通分支的大小比率:", ratio)
print("度数均值:", mean_degree)
print("度数标准差:", std_degree)

# 模块度
communities = greedy_modularity_communities(G)
mod_greed = nx.algorithms.community.modularity(G, communities)
print(f"贪心社区: {len(communities)}")
print(f"贪心模块度: {mod_greed}")
