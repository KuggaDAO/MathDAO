import pandas as pd
import csv
import numpy as np

# post with tags

# owneruserid: nan,have been deleted; -1,wiki
post = pd.read_csv("processed/posts.csv", usecols=['CreationDate', 'Id', 'PostTypeId', 'Tags', 'OwnerUserId', 'ParentId'], parse_dates=['CreationDate'])
post = post.dropna(subset=['OwnerUserId'])
post.loc[:, 'OwnerUserId'] = post['OwnerUserId'].astype(int)
post['Tags'] = post['Tags'].fillna('')

Tags = ['mathematica', 'numerical-linear-algebra', 'complex-numbers', 'probability-theory']
#count = [696, 3403, 18585, 42262]
#Tags = pd.read_csv("processed/tags.csv", usecols=['TagName']).values
#Tags = Tags[2:10].reshape(-1)
for tag in Tags:
    print(tag)
    questions = post[post['Tags'].str.contains(tag)]
    answers = post[post['ParentId'].isin(questions['Id'])]

    comment = pd.read_csv("processed/comments.csv", usecols=['CreationDate', 'Id', 'PostId', 'UserId'], parse_dates=['CreationDate'])
    comment = comment.dropna(subset=['UserId'])
    comment.loc[:, 'UserId']= comment['UserId'].astype(int)
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
    filename = tag+'qa.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(qa)
    print(f"CSV 文件 {filename} 已保存成功！")

    filename = tag+'qc.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(qc)
    print(f"CSV 文件 {filename} 已保存成功！")

    filename = tag+'ac.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ac)
    print(f"CSV 文件 {filename} 已保存成功！")
