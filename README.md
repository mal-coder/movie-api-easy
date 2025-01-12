--------------------
# Movie API
Simple REST API allowing requesting information about movies (but not necessarily limited to that).


With default configuration the user makes his requests using the API's **/** endpoint with query parameter *title={movie title}*.
Requests is authenticated with *Bearer token* provided by the user in *Authorization* header.
API queries for the title in the OMDB (https://www.omdbapi.com/), converts the response answer from XML to JSON and 
returns it to the user.  

## Prerequisites
(if you do not wish to install anything use the attached *docker-compose* file.):
* Python 3.9
* Pipenv

optionally: 
* Docker

optionally^2:
* The API is deployed to Heroku on:
```
https://movie-api-infor.herokuapp.com?title={movie title}
```


## Installing Movie API

To install File system API, follow these steps:
* Clone the repository and create a virtual environment with pipenv to install all the needed libraries
```
$ pipenv install
```
Create the following environmental variables or edit them in *docker-compose.yml*:
```
XML_API_URI=https://www.omdbapi.com/?r=xml&apikey=<your api key> - tagert server address !! remeber to update your API key
API_KEY=<applications key> - this is the key you'll be providing with the Authorization header
```
Optionally it is possible override additional settings:
```
XML_ATTRIBUTES=["title", "year", ...] - list of XML resposne attributes to be searched for
XML_QUERY_PARAMETER=t - query parameter for the target server
PORT=5000 - host port
HOST=0.0.0.0 - host address
QUERY_PARAMETER=title - query parameter name 
```

## Using Movie API

To use Movie API simply start it with:
```
python run.py 
```
Or use the provided `docker-compose.yml`:
```
docker-compose build
docker-compose up
```
For local deployment the default URL address is:
`http://0.0.0.0:5000/?title={movie title}`

For heroku the URL address is:
* `https://movie-api-infor.herokuapp.com?title={movie title}` 

If you don't know how or you're unable to make a request with *curl*, *Postman* you can use the heroku de:

`
https://reqbin.com/
`

** Remember to use *Authorization* header with token: `Bearer d1b9c69a-ec83-4bf4-9fac-c36ce4af47da`



The API has only one endpoint `/` and accepts `GET` request only.
Endpoint's description for default settings:
```
security:
  - bearerAuth: [ ]
paths:
  /:
    get:
      summary: "Retrieve movie information"
      parameters:
        - name: "title"
          in: query
          description: "Movie title"
          schema:
            type: "string"
            example: "Lost"
      responses:
        "200":
          description: "Data retrieved properly"
          content:
            application/json:
              schema:
                type: "object"
                example: {"title": "Lost",
                          "year": "2004–2010",
                          "rated": "TV-14",
                          "released": "22 Sep 2004",
                          "runtime": "44 min",
                          "genre": "Adventure, Drama, Fantasy, Mystery, Sci-Fi, Thriller",
                          "director": "N/A",
                          "writer": "J.J. Abrams, Jeffrey Lieber, Damon Lindelof",
                          "actors": "Jorge Garcia, Josh Holloway, Yunjin Kim, Evangeline Lilly",
                          "plot": "The survivors of a plane crash are forced to work together in order to survive on a seemingly deserted tropical island.",
                          "language": "English, Portuguese, Spanish, Arabic, French, Korean, German, Latin, Russian, Japanese",
                          "country": "USA",
                          "awards": "Won 1 Golden Globe. Another 112 wins &amp; 398 nominations.",
                          "poster": "https://m.media-amazon.com/images/M/MV5BNzhlY2E5NDUtYjJjYy00ODg3LWFkZWQtYTVmMzU4ZWZmOWJkXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
                          "metascore": "N/A",
                          "imdbRating": "8.3",
                          "imdbVotes": "498,563",
                          "imdbID": "tt0411008",
                          "type": "series"}
        "400":
          description: "Bad request"
        "401":
          description: "Token validation error"
        "404":
          description: "Movie not found"
        "500":
          description: "Server Error"
```

### Testing Movie API

To test Movie API run:
```
docker-compose run task2-api sh -c "pytest tests"
```
**Remember to update *docker-compose* XML_API_URI with your OMDB api key.

### Additional information
The application uses Flask framework with Flask-RESTful extension and Gunicorn WSGI server for deployment in 
production.

The reason for using a framework is to facilitate the very creation of the API and later on it's maintenance and
 possible extension.
 
By taking the advantage of working, secure, richly documented, constantly updated solutions which are supported by a huge 
community we can focus on the very core of our tasks - creating the part of the application containing logic for the 
business objectives and delivering reliable solutions faster.

Besides using the aforementioned framework the application uses Python standard libraries: *logging* for logging, 
*urllib.request* for handling requests and responses from target server and optionally *xml.etree*.
The *xml.etree* is not used actively - it's usage has to be enabled in the *config.py* file. 
By default all XML parsing is done "manually". 
