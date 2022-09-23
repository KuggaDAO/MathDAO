import pandas as pd
from .xml2csv import extract_user_data
from bs4 import BeautifulSoup

if __name__ == '__main__':

    print("begin extract users...")
    path = './xml/Users.xml'
    docs = BeautifulSoup(open(path), 'lxml')
    rows = docs.find_all('row')
    df_users = pd.DataFrame(list(map(extract_user_data, rows)))
    df_users.to_csv('./processed/users.csv', index=False)
    print("==end==")
