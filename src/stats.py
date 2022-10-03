import pandas as pd
for name in ['badges','comments','posts','tags','users','votes']:
    print(len(pd.read_csv('./processed/{}.csv'.format(name))))