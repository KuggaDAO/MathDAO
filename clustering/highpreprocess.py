import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, SpectralClustering
from sklearn.metrics import calinski_harabasz_score
import matplotlib.pyplot as plt
import numpy as np
import csv
from networkx.algorithms.community import greedy_modularity_communities

from randomwalk import *

QA = True
QC = True
AC = True
KMEANS = True
savefigs = False
thre = 0.999

# read data
user = pd.read_csv('processed/users.csv', usecols=['Id', 'Reputation'])
user['Id'] = user['Id'].astype(int)
# 计算声誉值的阈值
reputation_threshold = user['Reputation'].quantile(thre)  # 前0.1%的用户
# 选出声誉值大于阈值的用户
user = user[user['Reputation'] > reputation_threshold]
user_ids = user['Id'].tolist()
user_dict = user.set_index('Id').to_dict()['Reputation']


post = pd.read_csv("processed/posts.csv", usecols=['CreationDate', 'Id', 'PostTypeId', 'Tags', 'OwnerUserId', 'ParentId'], parse_dates=['CreationDate'])
# 筛选出owneruserid只包含给定用户id的数据
post = post.dropna(subset=['OwnerUserId'])
post.loc[:, 'OwnerUserId'] = post['OwnerUserId'].astype(int)
post = post[post['OwnerUserId'].isin(user_ids)]
questions = post[post['PostTypeId']==1.0]
answers = post[post['ParentId'].isin(questions['Id'])]

comment = pd.read_csv("processed/comments.csv", usecols=['CreationDate', 'Id', 'PostId', 'UserId'], parse_dates=['CreationDate'])
comment = comment.dropna(subset=['UserId'])
comment.loc[:, 'UserId']= comment['UserId'].astype(int)
comment = comment[comment['UserId'].isin(user_ids)]
coms_q = comment[comment['PostId'].isin(questions['Id'])]
coms_a = comment[comment['PostId'].isin(answers['Id'])]

qa = [] # question and answer
for _,row in answers.iterrows():
    parent_id = row['ParentId']
    question_row = questions[questions['Id'] == parent_id]
    if not question_row.empty:
        user_id = question_row.iloc[0]['OwnerUserId']
        qa.append([user_id, row['OwnerUserId'], row['CreationDate']])

qc = [] # question and comment
for _,row in coms_q.iterrows():
    post_id = row['PostId']
    question_row = questions[questions['Id'] == post_id]
    if not question_row.empty:
        user_id = question_row.iloc[0]['OwnerUserId']
        qc.append([user_id, row['UserId'], row['CreationDate']])

ac = [] # answer and comment
for _,row in coms_a.iterrows():
    post_id = row['PostId']
    answer_row = answers[answers['Id'] == post_id]
    if not answer_row.empty:
        user_id = answer_row.iloc[0]['OwnerUserId']
        ac.append([user_id, row['UserId'], row['CreationDate']])

# save
filename = 'highqa.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(qa)
print(f"CSV 文件 {filename} 已保存成功！")

filename = 'highqc.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(qc)
print(f"CSV 文件 {filename} 已保存成功！")

filename = 'highac.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(ac)
print(f"CSV 文件 {filename} 已保存成功！")