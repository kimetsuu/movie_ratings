import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t')
ratings = pd.read_csv('/Users/denisnovikov/Downloads/title.ratings.tsv', sep = '\t')

# # clean the data
# df = df.dropna()
# df['column_name'] = df['column_name'].fillna('default_value')

# df = df.drop_duplicates()

print(df.columns)
print(df.head())

# graph

region_counts = df['region'].value_counts()

region_counts.plot(kind = 'bar', figsize = (10, 5), color = 'skyblue')
plt.title('Number of Titles by Region')
plt.xlabel('Region')
plt.ylabel('Number of Titles')
plt.show()

region_counts.plot(kind = 'bar', figsize = (8, 5), color = 'skyblue')
plt.title('Most Popular Regions')
plt.xlabel('Region')
plt.ylabel('Number of Titles')
plt.show()

# stats models

mu, std = ratings['averageRating'].mean(), ratings['averageRating'].std()

plt.hist(ratings['averageRating'], bins = 10, density = True, alpha = 0.6, color = 'skyblue')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
plt.title(f'Normal Distribution Fit: μ = {mu:.2f}, σ = {std:.2f}')
plt.xlabel('Average Rating')
plt.ylabel('Density')
plt.show()