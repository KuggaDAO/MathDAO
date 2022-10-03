import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def draw_repu():
    df = pd.read_csv('./processed/users.csv')
    data = np.array(list(df.Reputation))

    histo = plt.hist(data, bins=40, log=True, density=False, rwidth=0.9, alpha=0.6)

    for idx, y in enumerate(histo[0]):
        plt.text(histo[1][idx], y*1.1, str(int(y)), fontsize=7)

    plt.xlabel("Reputation")
    plt.ylabel("log #people")
    plt.title("Reputation Distribution")
    plt.savefig('./figure/reputation.png')

def find_whale():
    df = pd.read_csv('./processed/users.csv')
    df = df.sort_values('Reputation', ascending=False)
    print(len(df))
    print(df[:3])
    id_lst = list(df.Id[:3])

    comments = pd.read_csv('./processed/comments.csv')
    posts = pd.read_csv('./processed/posts.csv')
    for id in id_lst:
        my_comment = comments[comments['UserId'] == id]
        my_posts = posts[posts['OwnerUserId'] == id]
        print("user {}: #comment {}, #post {}, #question {}, #answer {}".format(
            id,
            len(my_comment),
            len(my_posts),
            len(my_posts[my_posts['PostTypeId'] == 1.0]),
            len(my_posts[my_posts['PostTypeId'] == 2.0]),
        ))
        texts = list(my_comment.Text)
        with open('./misc/comment_text_{}.json'.format(id),'w') as f:
            import json
            json.dump(texts, f, ensure_ascii=False)


if __name__ == '__main__':
    find_whale()