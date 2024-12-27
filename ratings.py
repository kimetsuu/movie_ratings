import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t')

# clean the data
df = df.dropna()
df['column_name'] = df['column_name'].fillna('default_value')

df = df.drop_duplicates()


# print(df['genre'].value_counts())

# graph

# df['rating'].hist(bins=20)
# plt.xlabel('Rating')
# plt.ylabel('Frequency')
# plt.title('Distribution of Ratings')
# plt.show()

print(df.columns)
print(df.head())
