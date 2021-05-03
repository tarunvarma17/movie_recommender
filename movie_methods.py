import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title_caps == title]["index"].values[0]

def get_dir_from_index(index):
    return df[df.index == index]["director"].values[0]

df = pd.read_csv("Form Test\Data\movie_dataset.csv")

features = ['keywords','cast','genres','director']

for feature in features:
    df[feature] = df[feature].fillna('')

def combine_features(row):
    return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]

df["combined"] = df.apply(combine_features, axis =1)
df["title_caps"] = df["title"].str.title()

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined"])

cos = cosine_similarity(count_matrix)

df["release_date"] = pd.to_datetime(df["release_date"])
df["release_year"] = df["release_date"].dt.year

def content_rec(user_input):
    movie_index = get_index_from_title(user_input)
    similar_movies =  list(enumerate(cos[movie_index]))
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
    sorted_similar_movies = sorted_similar_movies[1:11]
    res = [lis[0] for lis in sorted_similar_movies]
    movs = [get_title_from_index(item) for item in res]
    #print(movs)
    return movs

def same_director(user_input):
    ind = get_index_from_title(user_input)
    user_dir = get_dir_from_index(ind)
    dir_df = df.loc[(df["director"] == user_dir) & (df["title"]!= user_input)]
    dir_df = dir_df.sort_values(by = ["vote_average"], ascending = False)
    dir_head_df = dir_df.head()
    dir_lis = dir_head_df["title"].tolist()
    return dir_lis

def rec_crit(sy, ey, genre, eng, anim):
    df_user = df.loc[(df["release_year"]>=sy) & (df["release_year"]<=ey)]
    if genre != "Any":
        df_user = df_user.loc[(df_user["genres"].str.contains(genre))]
    if eng:
        df_user = df_user.loc[(df["original_language"].str.contains("en"))]
    if anim:
        df_user = df_user.loc[(df["genres"].str.contains("Animation"))]
    df_user = df_user.sort_values(by = ["vote_average"], ascending = False).head(10)
    picklist = df_user["title"].tolist()
    if len(picklist) == 0:
        return ["Sorry, no movies match your criteria"]
    return picklist