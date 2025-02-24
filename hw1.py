# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO AUTOLAB

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW

    dict = {}
    with open(f, "r") as file:
        for line in file:
            arr = line.split('|')
            arr[0] = arr[0].strip()
            dict.setdefault(arr[0], [])
            dict[arr[0]] = dict.get(arr[0]) + [float(arr[1])]
    
    return dict
    

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW
    dict = {}

    with open(f, "r") as file:
        for line in file:
            arr = line.split('|')
            arr[0], arr[2] = arr[0].strip(), arr[2].strip()
            dict.update({arr[2]: arr[0]})
    
    return dict
    

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW
    
    newd = {}
    for k,v in d.items():
        newd.setdefault(v, [])
        newd[v] = newd[v] + [k]

    return newd
    
# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    newd = {}
    for k, v in d.items():
        newd.update({k: sum(v)/len(v)})
    return newd
    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW
    return {k:v for k,v in sorted(d.items(), key= lambda x: x[1], reverse=True)[:n]}
    

    
# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    return {k:v for k,v in d.items() if v >= thres_rating}
    
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    newd = {k:v for k,v in movie_to_average_rating.items() if k in genre_to_movies[genre]}
    return {k:v for k,v in sorted(newd.items(), key=lambda x: x[1], reverse=True)[:n]}
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    # WRITE YOUR CODE BELOW
    return sum([v for k,v in movie_to_average_rating.items() if k in {k:v for k,v in movie_to_average_rating.items() if k in genre_to_movies[genre]}])/len(genre_to_movies[genre])
    
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    # WRITE YOUR CODE BELOW
    return {k:v for k,v in sorted([(k, get_genre_rating(k, genre_to_movies, movie_to_average_rating)) for k,v in genre_to_movies.items()], key=lambda x: x[1], reverse=True)[:n]}

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    # WRITE YOUR CODE BELOW
    dict = {}
    with open(f, "r") as file:
        for line in file:
            arr = line.split('|')
            arr[0] = arr[0].strip()
            arr[2] = arr[2].strip("\n")

            dict.setdefault(arr[2], [])
            dict[arr[2]] = dict[arr[2]] + [(arr[0], arr[1])]
    
    return dict
    
    return dict
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW

    arr = [(movie_to_genre[k], v) for k,v in user_to_movies[user_id]]
    arr = sorted(arr, key=lambda x: x[0])
    curr = ""
    highest = 0
    hgenre = ""
    total = 0
    leng = 0
    # print(arr)
    for i,v in enumerate(arr):
        x,y = v
        if curr == "" or curr != x:
            if curr != "" and total/leng >= highest:
                highest = total/leng
                hgenre = curr
            curr = x
            total = float(y)
            leng = 1
        else:
            total += float(y)
            leng += 1
        if i == len(arr) -1:
            if curr != "" and total/leng >= highest:
                highest = total/leng
                hgenre = curr

    return hgenre
    

    
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    arr = [x for x,_ in user_to_movies[user_id]]
    movies_in_genre = [k for k,v in movie_to_genre.items() if v == top_genre and k not in arr]

    return {k:movie_to_average_rating[k] for k in sorted(movies_in_genre, key=lambda x: movie_to_average_rating[x], reverse=True)}

# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading
    pass
    
# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()

    
