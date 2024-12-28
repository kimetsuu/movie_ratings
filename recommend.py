import random 
import pandas as pd

df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t')
df_ratings = pd.read_csv('/Users/denisnovikov/Downloads/title.ratings.tsv', sep = '\t')

merged = pd.merge(df, df_ratings, left_on = 'titleId', right_on = 'tconst')

merged = merged[['titleId', 'title', 'averageRating', 'numVotes']]

min_rating = float(input('Enter the minimum rating: '))
n_movies = int(input('Enter the number of movies to recommend: '))

filtered_movies = merged[merged['averageRating'] >= min_rating]

selected = []
total = len(filtered_movies)

if total > n_movies:
    idx = []
    
    while len(idx) < n_movies:
        r_idx = random.randint(0, total - 1)
        if r_idx not in idx:
            idx.append(r_idx)
            
    for id in idx:
        selected.append(filtered_movies.iloc[id])
        
    selected_df = pd.DataFrame(selected)
    
else:
    print(f'Only {total} movies are available, showing all')
    selected_df = filtered_movies
    
print('\nSelected Movies:')
print(selected_df[['title', 'averageRating']])