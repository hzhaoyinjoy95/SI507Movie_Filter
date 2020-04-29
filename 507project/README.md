# Brief Instruction

## Introduction
The project mainly uses flask to satisfy user interaction using various graphs, plots and tables to present information.

## How to supply API keys:
Request for free api for the open movie database through this link:
http://www.omdbapi.com/apikey.aspx

## How to interact with your program.
- User will be greeted with a welcome page, which allows a user to fill in a name and choose a movie genre to filter. I like the “No Idea” option which allows users to get random choice of movies from the database. 
- Following a search, a user will see a page with three movie posters and link to more detailed information about the movies. User could choose to go back to search again or check out the movie database.
- If a user click on one of the poster, there will be a detailed page of movie information. It also includes links for rating plot if there are ratings from three sources, links to IMDB for directors, writers, stars and the movie itself. User can direct back to the homepage through the bottom link.
- If a user choose to check out the movie database, he or she will see a list of movies presented with movie’s names, year, rated and a link to a more detailed information page as described above. 

## Required packages:
- flask
- sqlite3
- plotly
