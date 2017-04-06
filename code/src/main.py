## Created by Rasmus Munk ##
## Requires that a root dir is given, every .dat file in this directory is loaded into memory using ...
import argparse, os
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Movie Ratings Analyser', fromfile_prefix_chars='@')
parser.add_argument('-rd','--rootdir', action='store', required=True, help="The path to the directory containing the files to be analysed")
args = parser.parse_args()

# Uses panda to load the file in as a DataFrame
def load_data(file_path, header):
    data = pd.read_table(file_path, sep='::', header=None, names=header, engine='python')
    return data

## Defines the header each dataframe has
def define_header(filename):
    header = []
    if filename == 'ratings.dat':
        header = ['user_id', 'movie_id', 'rating', 'timestamp']
    elif filename == 'users.dat':
        header = ['user_id','gender','age','occupation','zip']
    elif filename == 'movies.dat':
        header = ['movie_id', 'title', 'genres']

    if len(header) < 1:
        print("A header was not defined for this file: " + filename)
        exit(-1)

    return header


## Walks the passed directory and calls load_data for each file that ends with .dat
## Returns a list of dataframes
def load_dat_in_dir(directory_path):
    list_data_frames = []
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            if name.endswith('.dat'):
                header = define_header(name)
                list_data_frames.append(load_data(os.path.join(root,name), header))

    if len(list_data_frames) < 1:
        print("No valid datafiles were found in: " + directory_path)
        exit(-1)

    return list_data_frames

## Merges the list of data frames into one big dataframe object
## requires that each frame has a common column that can be used for the merger -> foreign keys
def merge_dataframes(list_data_frames):
    final_frame = list_data_frames[0]
    for idx, data_frame in enumerate(list_data_frames):
        if idx > 0:
            final_frame = pd.merge(data_frame, final_frame)

    return final_frame

## Returns a series with either the titles that are above or below the provided target_average -> determined by b_above
def ab_average_rating_value(data_frame, target_average, b_above):
    average_rating = data_frame.groupby('title').rating.mean()
    average_rating = average_rating.dropna()
    if b_above:
        above_target_average = average_rating.index[average_rating > target_average]
    else:
        above_target_average = average_rating.index[average_rating < target_average]
    return above_target_average


if __name__ == "__main__":
    print("---- Question 1 ----")
    ## Answer num 1
    list_data_frames = load_dat_in_dir(args.rootdir)
    merged_data_frame = merge_dataframes(list_data_frames)
    above_average = ab_average_rating_value(merged_data_frame, 4, b_above=True)

    print("How many movies have an average rating over 4: " + str(len(above_average)))

    print("---- Question 2 ----")
    ## Answer num 2
    men_ratings = merged_data_frame.loc[merged_data_frame['gender'] == 'M']
    men_above_average = ab_average_rating_value(men_ratings, 4, b_above=True)
    print("How many movies have been rated by men over 4 on average: " + str(len(men_above_average)))

    print("---- Question 3 ----")
    ## Answer num 3
    women_ratings = merged_data_frame.loc[merged_data_frame['gender'] == 'F']
    women_below_average = ab_average_rating_value(women_ratings, 4, b_above=False)
    print("How many movies have been rated by women below 4 on average: " + str(len(women_below_average)))

    print("---- Question 4 ----")
    ## Answer Num 4
    ## What makes a top movie
    num_ratings_movie = merged_data_frame.groupby('title').size()
    ## Key Stats
    print("Rating mean: " + str(num_ratings_movie.mean()))
    print("Rating std: " + str(num_ratings_movie.std()))
    print("Rating median: " + str(num_ratings_movie.median()))
    print("Rating skew: " + str(num_ratings_movie.skew()))

    ## Bottom heavy -> positive skew, median is lower than the mean
    print("---- The top movies are ----")
    movies_top_ratings = num_ratings_movie.index[num_ratings_movie >= 300]
    top_movies = merged_data_frame.groupby('title').rating.mean()
    top_movies = top_movies.ix[movies_top_ratings]
    top_movies = top_movies.sort_values(ascending=False, axis=0)
    print("Number of applicable movies: " + str(len(top_movies)))
    print(top_movies[:10])



    ## Plot histogram
    #
    # fig = plt.figure()
    # num_ratings_movie.plot.hist(stacked=True)
    # fig.suptitle("Histogram of Movie Ratings", fontsize=20)
    # plt.xlabel('Number of Ratings')
    # plt.ylabel('Frequency')
    # plt.show(block=True)