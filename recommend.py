import random 
import pandas as pd

'''Use a class to differentiate between different functions'''
class TaskBar:
    def __init__(self):
        self.df = pd.read_csv('/Users/denisnovikov/Downloads/title.akas.tsv', sep = '\t').sample(frac = 0.25, random_state = 42)        # random_state is used to reproduce the same random values
        self.df_ratings = pd.read_csv('/Users/denisnovikov/Downloads/title.ratings.tsv', sep = '\t').sample(frac = 0.25, random_state = 42)     # the number 42 does not have any significance,
        self.df_genres = pd.read_csv('/Users/denisnovikov/Downloads/title.basics.tsv', sep = '\t', low_memory = False).sample(frac = 0.25, random_state = 42)   # its just a common practice to use it
        
        merged = pd.merge(self.df, self.df_ratings, left_on = 'titleId', right_on = 'tconst')           # merge the dataframes 
        merged = pd.merge(merged, self.df_genres, left_on = 'titleId', right_on = 'tconst')             
        self.merged = merged[['titleId', 'title', 'averageRating', 'numVotes', 'titleType', 'genres']]  # select the required columns


    '''Recommend movies based on user input'''
    def recommend(self):
        min_rating = float(input('Enter the minimum rating: '))
        n_movies = int(input('Enter the number of movies to recommend: '))
        movie_type = input('Enter the movie type (movie, short, tvseries, tvepisode, video): ')
        genre = input('Enter the genre: ')

        filtered_movies = self.merged[                                      # filter the movies based on the user input
            (self.merged['averageRating'] >= min_rating) & 
            (self.merged['titleType'].str.lower() == movie_type.lower()) & 
            (self.merged['genres'].str.lower().fillna('').apply(lambda g: genre.lower() in g.split(',')))
        ]

        selected = []
        total = len(filtered_movies)

        if total > n_movies:
            idx = []
            
            while len(idx) < n_movies:                  # select n random movies
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
    
    '''Show top genres based on average rating'''    
    def show_top_genres(self):
        self.merged['genres'] = self.merged['genres'].str.lower().fillna('')
        
        genre_rating = {}
        
        for _, row in self.merged.iterrows():       # .iterrows() generates an iterator of (index, Series) pairs
            genres = row['genres'].split(',')       # split the genres by comma
            rating = row['averageRating']
            
            for genre in genres:                    # iterate through each genre
                if genre not in genre_rating:       
                    genre_rating[genre] = {'total_rating': 0, 'count': 0}   # initialize the genre if not present
                genre_rating[genre]['total_rating'] += rating 
                genre_rating[genre]['count'] += 1
                
        average_rating = {}                                   # calculate the average rating for each genre
        for genre, genre_rating in genre_rating.items():        
            if genre_rating['count'] > 0:
                average_rating[genre] = genre_rating['total_rating'] / genre_rating['count']    # average rating = total rating / count
                
                
        
        print('\nTop Genres:')
        for genre, rating in average_rating.items():
            print(f'{genre}: {rating:.2f}')
    
    '''Run the taskbar'''
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