import random 
import pandas as pd

df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t')
df_ratings = pd.read_csv('/Users/denisnovikov/Downloads/title.ratings.tsv', sep = '\t')
df_genres = pd.read_csv('/Users/denisnovikov/Downloads/title.basics.tsv', sep = '\t', low_memory = False)

merged = pd.merge(df, df_ratings, left_on = 'titleId', right_on = 'tconst')
merged = pd.merge(merged, df_genres, left_on = 'titleId', right_on = 'tconst')

merged = merged[['titleId', 'title', 'averageRating', 'numVotes', 'titleType', 'genres']]

min_rating = float(input('Enter the minimum rating: '))
n_movies = int(input('Enter the number of movies to recommend: '))
movie_type = input('Enter the movie type (movie, short, tvseries, tvepisode, video): ')
genre = input('Enter the genre: ')

filtered_movies = merged[
    (merged['averageRating'] >= min_rating) & 
    (merged['titleType'].str.lower() == movie_type.lower()) & 
    (merged['genres'].str.lower().fillna('').apply(lambda g: genre.lower() in g.split(',')))
]

print(len(filtered_movies))


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
print(selected_df[['title', 'averageRating', 'titleType', 'genres']])