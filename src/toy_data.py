import pandas as pd
for name in ['badges','posts','users','votes','comments']:
    df = pd.read_csv('./processed/{}.csv'.format(name))
    toy = df[:100]
    toy.to_csv('./toy_data/{}.csv'.format(name))
