import random 
import pandas as pd

class TaskBar:
    def __init__(self):
        self.df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t')
        self.df_ratings = pd.read_csv('/Users/denisnovikov/Downloads/title.ratings.tsv', sep = '\t')
        self.df_genres = pd.read_csv('/Users/denisnovikov/Downloads/title.basics.tsv', sep = '\t', low_memory = False)
        
        merged = pd.merge(self.df, self.df_ratings, left_on = 'titleId', right_on = 'tconst')
        merged = pd.merge(merged, self.df_genres, left_on = 'titleId', right_on = 'tconst')
        self.merged = merged[['titleId', 'title', 'averageRating', 'numVotes', 'titleType', 'genres']]

    def recommend(self):
        min_rating = float(input('Enter the minimum rating: '))
        n_movies = int(input('Enter the number of movies to recommend: '))
        movie_type = input('Enter the movie type (movie, short, tvseries, tvepisode, video): ')
        genre = input('Enter the genre: ')

        filtered_movies = self.merged[
            (self.merged['averageRating'] >= min_rating) & 
            (self.merged['titleType'].str.lower() == movie_type.lower()) & 
            (self.merged['genres'].str.lower().fillna('').apply(lambda g: genre.lower() in g.split(',')))
        ]

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
        
    def show_top_genres(self):
        pass
    
    def run(self):
        while True:
            print('\nWhat would you like to do?')
            print('1. Recommend Movies')
            print('2. Show Top Genres')
            print('0. Exit')
            
            choice = int(input('Enter your choice: '))
            
            if choice == 1:
                self.recommend()
            elif choice == 2:
                self.show_top_genres()
            elif choice == 0:
                print('Exiting...')
                break
            else:
                print('Invalid input')
                
if __name__ == '__main__':
    taskbar = TaskBar()
    taskbar.run()