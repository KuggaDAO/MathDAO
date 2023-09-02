from sklearn.cluster import KMeans
import pandas as pd
import networkx as nx
from gensim.models import Word2Vec
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import csv
from sklearn.preprocessing import StandardScaler

from randomwalk import *

def weighted_kmeans_plusplus(X, weights, n_clusters, max_iter=300):
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=max_iter)
    kmeans.fit(X, sample_weight=weights)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    return centers, labels

QA = True
QC = True
AC = True
WEIGHT = False
#Tags = ['mathematica', 'numerical-linear-algebra', 'complex-numbers', 'probability-theory']
#count = [696, 3403, 18585, 42262]
Tags = pd.read_csv("processed/tags.csv", usecols=['TagName']).values
Tags = Tags[3:10].reshape(-1)
#Tags = ['mathematica']

# read data
user = pd.read_csv('processed/users.csv', usecols=['Id', 'Reputation'])
user['Id'] = user['Id'].astype(int)
user_dict = user.set_index('Id').to_dict()['Reputation']

for tag in Tags:
    qa = pd.read_csv(tag+'qa.csv', header=None, names=['user1','user2','time'])
    qc = pd.read_csv(tag+'qc.csv', header=None, names=['user1','user2','time'])
    ac = pd.read_csv(tag+'ac.csv', header=None, names=['user1','user2','time'])

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

    walks = generate_walks(G, num_walks=10, walk_length=80)

    embedding_size = 64
    window_size = 10
    min_count = 5

    # 使用Word2Vec训练节点序列
    model = Word2Vec(walks, vector_size=embedding_size, window=window_size, min_count=min_count)

    # 将嵌入向量转换为数组，并标准化
    X = model.wv.vectors
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    nodes = np.array(list(G.nodes()))
    reputations = [user_dict[node] for node in nodes]
    weights = (reputations - np.min(reputations))/(np.max(reputations)-np.min(reputations))

    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)

    sselist = []
    for n_clusters in range(2,10):
        if WEIGHT:
            centers, labels = weighted_kmeans_plusplus(X_reduced, weights, n_clusters, max_iter=300)
        else:
            kmeans = KMeans(n_clusters, init='k-means++', max_iter=300)
            kmeans.fit(X_reduced)
            centers = kmeans.cluster_centers_
            labels = kmeans.labels_
        sse = 0
        for i in range(n_clusters):
            cluster_samples = X_reduced[labels == i]
            cluster_center = centers[i]
            cluster_sse = np.sum((cluster_samples - cluster_center) ** 2)
            sse += cluster_sse
        sselist.append(sse)

    # plot
    #plt.plot(np.arange(2,10), sselist)
    #plt.show()

    dsse2 = -np.diff(sselist,n=2)
    nclus = np.where(dsse2<0)[0][0]+3
    centers, labels = weighted_kmeans_plusplus(X_reduced, weights, nclus, max_iter=300)
    sse = 0
    cluseruser = []
    stat = []
    print(tag)
    for i in range(nclus):
        cluster_samples = X_reduced[labels == i]
        cluster_center = centers[i]
        cluster_sse = np.sum((cluster_samples - cluster_center) ** 2)
        sse += cluster_sse

        user = nodes[labels==i]
        size = len(user)
        cluseruser.append(user)

        rep = [user_dict[i] for i in user]
        rmax = np.max(rep)
        rmean = np.mean(rep)
        rstd = np.std(rep)
        stat.append([i,size,rmax,rmean,rstd])
        print(f"i:{i}, size:{size}, rmax:{rmax}, rmean:{rmean},rstd:{rstd}")

    # save
    filename = './result/'+tag+'clusteruser.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(cluseruser)
    print(f"CSV 文件 {filename} 已保存成功！")
    filename = './result/stat/'+tag+'stat.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stat)
    print(f"CSV 文件 {filename} 已保存成功！")

    n = len(reputations)
    k = int(0.001 * n)  # 计算前0.1%的数的个数
    sorted_indices = np.argsort(reputations)  # 对数值列表进行排序并返回索引数组
    top_percent_indices = sorted_indices[-k:]

    fig = plt.figure()
    cmap = plt.get_cmap('tab10') # 颜色映射
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, cmap=cmap, alpha=0.7)
    plt.scatter(X_reduced[top_percent_indices, 0], X_reduced[top_percent_indices, 1], c='r', alpha=0.7)
    for i in range(nclus):
        plt.annotate(str(i), xy=(centers[i][0],centers[i][1]), c='k')
    plt.title(f"tag={tag}, ncluster={nclus}, sse={int(sse)}")
    plt.savefig('./result/fig/'+tag+'.png')