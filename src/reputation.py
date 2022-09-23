import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./processed/users.csv')
data = np.array(list(df.Reputation))

histo = plt.hist(data, bins=40, log=True, density=False, rwidth=0.9, alpha=0.6)

for idx, y in enumerate(histo[0]):
    plt.text(histo[1][idx], y*1.1, str(int(y)), fontsize=7)

plt.xlabel("Reputation")
plt.ylabel("log #people")
plt.title("Reputation Distribution")
plt.savefig('./figure/reputation.png')
