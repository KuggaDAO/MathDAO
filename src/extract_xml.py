import pandas as pd
from xml2csv import extract_user_data, process_line_post, extract_badge_data, process_line_votes, extract_comments_data, extract_tags_data
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--xml', type=str, default='users', choices=['users', 'posts', 'badges', 'votes', 'comments', 'tags'])
args = parser.parse_args()

if __name__ == '__main__':

    if args.xml == 'users':
        path = './xml/Users.xml'
        docs = BeautifulSoup(open(path), 'lxml')
        rows = docs.find_all('row')
        df_users = pd.DataFrame(list(map(extract_user_data, rows)))
        df_users.to_csv('./processed/users.csv', index=False)

    elif args.xml == 'posts':
        path = './xml/Posts.xml'
        with open(path) as f:
            df_posts = pd.DataFrame(list(map(process_line_post, f.readlines())))
            df_posts.to_csv('./processed/posts.csv', index=False)
    
    elif args.xml == 'badges':
        path = './xml/Badges.xml'
        docs = BeautifulSoup(open(path), 'lxml')
        rows = docs.find_all('row')
        df_badges = pd.DataFrame(list(map(extract_badge_data, rows)))
        df_badges.to_csv('./processed/badges.csv', index=False)
    
    elif args.xml == 'votes':
        path = './xml/Votes.xml'
        with open(path) as f:
            df_votes = pd.DataFrame(list(map(process_line_votes, f.readlines())))
            df_votes.to_csv('./processed/votes.csv', index=False)

    elif args.xml == 'comments':
        path = './xml/Comments.xml'
        docs = BeautifulSoup(open(path), 'lxml')
        rows = docs.find_all('row')
        df_comments = pd.DataFrame(list(map(extract_comments_data, rows)))
        df_comments.to_csv('./processed/comments.csv', index=False)
    
    elif args.xml == 'tags':
        path = './xml/Tags.xml'
        docs = BeautifulSoup(open(path), 'lxml')
        rows = docs.find_all('row')
        df_tags = pd.DataFrame(list(map(extract_tags_data, rows)))
        df_tags.to_csv('./processed/tags.csv', index=False)
