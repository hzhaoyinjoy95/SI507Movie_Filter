from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objs as go 

DB_NAME = 'movies_people_copy.sqlite'

app = Flask(__name__)


def get_movie_by_genre(genre):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if genre == 'No_preference':
        q = f'''
        SELECT Title, Year, imdbId, PosterURL 
        FROM Movie 
        WHERE id 
        IN (SELECT id FROM Movie ORDER BY RANDOM() LIMIT 3)
        '''
    else:
        q = f'''
        SELECT Title, Year, imdbId, PosterURL 
        FROM Movie
        WHERE Genre1 = '{genre}'
        LIMIT 3
        '''

    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_movie_detail_three(title):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    q = f'''
    SELECT *
    FROM Movie 
    WHERE Title = '{title}'
    '''

    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_crew_detail(id_crew):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    q = f'''
    SELECT *
    FROM Crew 
    WHERE Id = '{id_crew}'
    '''

    results = cur.execute(q).fetchall()
    conn.close()
    return results

def plot_rating_bar(ratings):
    xvals = ['Internet Movie Database', 'Rotten Tomatoes', 'Metacritic']
    percent1 = ratings[0]['Value'].split('/')
    percent_1 = float(percent1[0])/int(percent1[1])*100
    percent2 = ratings[1]['Value'].split("%")
    percent_2 = int(percent2[0])
    percent3 = ratings[2]['Value'].split('/')
    percent_3 = float(percent3[0])/int(percent3[1])*100
    yvals = [percent_1, percent_2, percent_3]

    bar_data = go.Bar(x=xvals, y=yvals)
    basic_layout = go.Layout(title="Rating Bar(%)")
    fig = go.Figure(data=bar_data, layout=basic_layout)
    div = fig.to_html(full_html=False)
    return div

@app.route('/')
def welcome():
    return render_template('filter_index.html')

@app.route('/filter_response', methods=['POST'])
def response():
    name = request.form["name"]
    genre = request.form["genre"]
    results = get_movie_by_genre(genre)

    return render_template('filter_response.html', 
        name=name, 
        genre=genre,
        results = results
        )

@app.route('/more_movies/<name>')
def movie_list(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    q = f'''
    SELECT Title, Year, Rated
    FROM Movie 
    '''

    results = cur.execute(q).fetchall()
    conn.close()
    return render_template('list_movies.html', 
        name=name, 
        results = results
        )

@app.route('/movie_detail/<title>')
def movie_detail(title):
    #getting movie basic info
    detail = get_movie_detail_three(title)

    #getting rating info
    results = get_movie_detail_three(title)[0]
    ratings = eval(results[8])
    ratinglist = []
    for rating in ratings:
        source = rating['Source']
        rating = rating['Value']
        one_rating = f"{source}: {rating}"
        ratinglist.append(one_rating)
    len_ratings = len(ratings)
    
    #getting crew info
    director_info = get_crew_detail(detail[0][10])
    writer_info = get_crew_detail(detail[0][12])
    star_info1 = get_crew_detail(detail[0][15])
    star_info2 = get_crew_detail(detail[0][16])
    star_info3 = get_crew_detail(detail[0][17])
    star_info4 = get_crew_detail(detail[0][18])

    #check length to determine whether to display or not
    len_director = len(director_info)
    len_writer = len(writer_info)
    len_star1 = len(star_info1)
    len_star2 = len(star_info2)
    len_star3 = len(star_info3)
    len_star4 = len(star_info4)

    return render_template('movie_detail.html', 
        title=title, 
        ratings=ratinglist,
        len_ratings=len_ratings,
        detail=detail,
        director_info=director_info,
        writer_info=writer_info,
        star_info1=star_info1,
        star_info2=star_info2,
        star_info3=star_info3,
        star_info4=star_info4,
        len_director=len_director,
        len_writer=len_writer,
        len_star1=len_star1,
        len_star2=len_star2,
        len_star3=len_star3,
        len_star4=len_star4,
        )


@app.route('/movie_detail/<title>/plot')
def plot(title):
    results = get_movie_detail_three(title)[0]
    print(results)
    ratings = eval(results[8])
    xvals = ['Internet Movie Database', 'Rotten Tomatoes', 'Metacritic']
    percent1 = ratings[0]['Value'].split('/')
    percent_1 = float(percent1[0])/int(percent1[1])*100
    percent2 = ratings[1]['Value'].split("%")
    percent_2 = int(percent2[0])
    percent3 = ratings[2]['Value'].split('/')
    percent_3 = float(percent3[0])/int(percent3[1])*100
    yvals = [percent_1, percent_2, percent_3]

    bar_data = go.Bar(x=xvals, y=yvals)
    basic_layout = go.Layout(title="Rating Bar(%)")
    fig = go.Figure(data=bar_data, layout=basic_layout)
    div = fig.to_html(full_html=False)
    return render_template("plot.html", plot_div=div)


if __name__ == "__main__":
    app.run(debug=True)
