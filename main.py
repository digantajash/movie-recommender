import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request

#functions
def combine_features(row):
    return row['Rank']+" "+row['Title']+" "+row['Score']+" "+row['Genre']+" "+row['Director']  

def get_title_from_rank(Rank):
    return data[data.Rank==Rank]["Title"].values[0]

def get_rank_from_title(Title):
    return data[data.Title==Title]["Rank"].values[0]

def sim_score():
    CV=CountVectorizer()
    X=CV.fit_transform(data["combined_features"])
    similarity_scores = cosine_similarity(X)
    return similarity_scores

def movierec(mov):
    if mov not in data['Title'].unique():
        return('this movie is not in our database')
    else:
        similarity_scores = sim_score()
        movie_rank=int(get_rank_from_title(mov))
        similar_movies=list(enumerate(similarity_scores[movie_rank]))
        sorted_films=sorted(similar_movies,key=lambda a:a[1],reverse=True)[1:]
        i=0
        recommendation=[]
        for element in sorted_films :
            recom=get_title_from_rank(str(element[0]))
            recommendation.append(recom)
            i=i+1
            if i>=5:
                 break
    return recommendation

#data processing

sample_data=pd.read_csv('movies.csv')
data=pd.DataFrame(sample_data,columns=['Rank','Title','Score','Genre','Director'])
data=data.astype(str)
data["combined_features"]=data.apply(combine_features,axis=1)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/recommend',methods=['GET'])
def recommend():
    movie = request.args.get('movie')
    recom = movierec(movie)
    if type(recom) == type('string'):
        return render_template('recommend.html',movie=movie,recom=recom,y='y')
    else:
         return render_template('recommend.html',movie=movie,recom=recom,y='n')


if __name__ == '__main__':
    app.run()
